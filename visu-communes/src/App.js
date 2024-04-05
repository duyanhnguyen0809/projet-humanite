import React from "react";
import Navbar from "./components/Navbar";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import Modifications from "./pages/Modifications";
import Fusions from "./pages/Fusions";
import Creations from "./pages/Creations";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/Modifications" element={<Modifications />} />
        <Route path="/Fusions" element={<Fusions />} />
        <Route path="/Creations" element={<Creations />} />
      </Routes>
    </Router>
  );
}
export default App;
