import React from "react";
import "../App.css";
import { Button } from "./Button";
import "./HeroSection.css";
import { Link } from "react-router-dom";

function HeroSection() {
  return (
    <div className="hero-container">
      <video src="/video/video-2.mp4" autoPlay loop muted />
      <h1>L'AVENTURE ATTEND</h1>
      <p>Qu'est-ce que tu attends?</p>
      <div className="hero-btns">
        <Link to="/modifications">
          <Button
            className="btns"
            buttonStyle="btn--outline"
            buttonSize="btn--large"
          >
            COMMENCER
          </Button>
        </Link>
        <Link to="/about">
          <Button
            className="btns"
            buttonStyle="btn--primary"
            buttonSize="btn--large"
            onClick={console.log("hey")}
          >
            ABOUT US <i className="far fa-play-circle" />
          </Button>
        </Link>
      </div>
    </div>
  );
}

export default HeroSection;
