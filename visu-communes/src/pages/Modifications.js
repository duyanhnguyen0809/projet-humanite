import React, { useState, useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import './Calendar.css';


const new_marker = process.env.PUBLIC_URL + "/icons/new_marker.svg";
const old_marker = process.env.PUBLIC_URL + "/icons/old_marker.svg";
function Modifications() {
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
        const newMap = L.map(mapContainer.current).setView(
          [46.603354, 1.888334],
          5
        );
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
          .bindPopup(`<a href="${commune.url}">${commune.nom}</a>`);
      });
      nouvelleCommunes.forEach((commune) => {
        L.marker([commune.lat, commune.lon], {
          icon: L.icon({ iconUrl: new_marker, iconSize: [30, 30] }),
        })
          .addTo(map)
          .bindPopup(`<a href="${commune.url}">${commune.nom}</a>`);
      });
    }
  }, [map, ancienneCommunes, nouvelleCommunes]);

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
        <div style={{
          flexDirection: "column",
          display: "flex",
          gap: "10px",
          justifyContent: "center",
        }}>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="date-input"
          />
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="date-input"
          />
          <button onClick={handleClick}>Show Changes</button>
        </div>
      </div>
      {showMap && (
        <div
          ref={mapContainer}
          style={{ height: "500px", width: "100%" }}
        ></div>
      )}
    </div>
  );
}

export default Modifications;
