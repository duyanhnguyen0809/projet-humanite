import React, { useState, useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./Calendar.css";
import "./Modifications.css";
import { renderToString } from "react-dom/server";
const BindPopupOld = ({ nom, url }) => {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "3px" }}>
      <div>Ancienne commune: </div>
      <a href={url}>{nom}</a>
    </div>
  );
};
const BindPopupNew = ({ nom, url }) => {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "3px" }}>
      <div>Nouvelle commune: </div>
      <a href={url}>{nom}</a>
    </div>
  );
};

function Modifications() {
  const new_marker = process.env.PUBLIC_URL + "/icons/new_marker.svg";
  const old_marker = process.env.PUBLIC_URL + "/icons/old_marker.svg";
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [events, setEvents] = useState([]);
  const [ancienneCommunes, setAncienneCommunes] = useState([]);
  const [nouvelleCommunes, setNouvelleCommunes] = useState([]);
  const [map, setMap] = useState(null);
  const [showMap, setShowMap] = useState(false);
  const mapContainer = useRef(null);

  const handleClick = () => {
    fetch(
      process.env.REACT_APP_GLOBAL_PORT +
        `/api/modifications/${startDate}/${endDate}`
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => setEvents(data))
      .catch((error) => console.error("Error:", error));
    setShowMap(true);
  };
  useEffect(() => {
    const fetchCommunes = async () => {
      const uniqueNewIds = [
        ...new Set(events.map((event) => event.id_nouveau)),
      ];
      const newCommunes = await Promise.all(
        uniqueNewIds.map(async (id) => {
          const response = await fetch(
            process.env.REACT_APP_GLOBAL_PORT + `/api/communes/${id}`
          );
          const commune = await response.json();
          return commune[0];
        })
      );
      setNouvelleCommunes(newCommunes);
    };
    fetchCommunes();
  }, [events]);

  useEffect(() => {
    const fetchCommunes = async () => {
      const uniqueOldIds = [...new Set(events.map((event) => event.id_ancien))];
      const oldCommunes = await Promise.all(
        uniqueOldIds.map(async (id) => {
          const response = await fetch(
            process.env.REACT_APP_GLOBAL_PORT + `/api/communes/${id}`
          );
          const commune = await response.json();
          return commune[0];
        })
      );
      setAncienneCommunes(oldCommunes);
    };
    fetchCommunes();
  }, [events]);
  useEffect(() => {
    const initializeMap = () => {
      if (showMap && !map) {
        const newMap = L.map(mapContainer.current).setView([43.92, 7.17], 7);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(
          newMap
        );
        setMap(newMap);
      }
    };

    initializeMap();
  }, [map, showMap]);

  useEffect(() => {
    if (map) {
      ancienneCommunes.forEach((commune) => {
        L.marker([commune.lat + 0.0001, commune.lon], {
          icon: L.icon({ iconUrl: old_marker, iconSize: [30, 30] }),
        })
          .addTo(map)
          .bindPopup(
            renderToString(<BindPopupOld nom={commune.nom} url={commune.url} />)
          );
      });
      nouvelleCommunes.forEach((commune) => {
        L.marker([commune.lat, commune.lon], {
          icon: L.icon({ iconUrl: new_marker, iconSize: [30, 30] }),
        })
          .addTo(map)
          .bindPopup(
            renderToString(<BindPopupNew nom={commune.nom} url={commune.url} />)
          );
      });
    }
  }, [map, ancienneCommunes, nouvelleCommunes, new_marker, old_marker]);

  return (
    <div>
      <div
        style={{
          height: "300px",
          width: "100vw",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            flexDirection: "column",
            display: "flex",
            gap: "10px",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <h1>MODIFICATIONS DES COMMUNES</h1>

          <div>
            <label
              style={{ color: "white", fontWeight: "bold", fontSize: "1rem" }}
            >
              Du :{" "}
            </label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="date-input"
            />
          </div>
          <div>
            <label
              style={{ color: "white", fontWeight: "bold", fontSize: "1rem" }}
            >
              Au :{" "}
            </label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="date-input"
            />
          </div>
          <button
            style={{
              backgroundColor: "#1dd1a1",
              color: "white",
              padding: "10px",
              borderRadius: "5px",
              marginTop: "10px",
            }}
            onClick={handleClick}
          >
            Show Changes
          </button>
        </div>
      </div>
      {showMap && <div ref={mapContainer} className="map-container"></div>}
      {showMap && (
        <table className="table">
          <thead>
            <tr>
              <th>Nouvelle Commune</th>
              <th>Ancienne Commune</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event, index) => {
              const newCommune = nouvelleCommunes.find(
                (commune) => commune.id === event.id_nouveau
              );
              const reunitedCommune = ancienneCommunes.find(
                (commune) => commune.id === event.id_ancien
              );
              return (
                <tr key={index}>
                  <td>{newCommune ? newCommune.nom : "Not found"}</td>
                  <td>{reunitedCommune ? reunitedCommune.nom : "Not found"}</td>
                  <td>{new Date(event.date).toLocaleDateString()}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Modifications;
