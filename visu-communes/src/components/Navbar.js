import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";
import { faHome, faFaceSmile } from "@fortawesome/free-solid-svg-icons";
import { faThinkPeaks } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function Navbar() {
  const [click, setClick] = useState(false);
  const handleClick = () => setClick(!click);
  const closeMobileMenu = () => setClick(false);

  const showButton = () => {
    if (window.innerWidth <= 960) {
      setClick(false);
    } else {
      setClick(true);
    }
  };

  window.addEventListener("resize", showButton);

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-logo" onClick={handleClick}>
            <a href="/">VisuCommunes</a> <FontAwesomeIcon icon={faThinkPeaks} />
          </Link>
          <ul>
            <li className="nav-item">
              <Link to="/" className="nav-links" onClick={closeMobileMenu}>
                <FontAwesomeIcon icon={faHome} /> Home
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/about" className="nav-links">
                <FontAwesomeIcon icon={faFaceSmile} /> About Us
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/modifications" className="nav-links">
                <FontAwesomeIcon icon={faFaceSmile} /> Modifications
              </Link>
            </li>
          </ul>
        </div>
      </nav>
    </>
  );
}

export default Navbar;
