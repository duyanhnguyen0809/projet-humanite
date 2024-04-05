const express = require("express");
const app = express();
const port = 8000;

app.get("/", (req, res) => {
  res.send("Hello World!");
});
const cors = require("cors");

app.use(cors());
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

const mysql = require("mysql2");

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "chop1234",
  database: "projet_humanite",
});

app.get("/api/communes", (req, res) => {
  db.query("SELECT * FROM communes", (err, results) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(results);
  });
});

app.get("/api/communes/:id", (req, res) => {
  db.query(
    "SELECT * FROM communes WHERE id = ?",
    [req.params.id],
    (err, results) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json(results);
    }
  );
});

app.get("/api/modifications/:startDate/:endDate", (req, res) => {
  const { startDate, endDate } = req.params;
  db.query(
    "SELECT * FROM modifications WHERE date >= ? AND date <= ?",
    [startDate, endDate],
    (err, results) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json(results);
    }
  );
});


app.get("/api/fusions/:startDate/:endDate", (req, res) => {
  const { startDate, endDate } = req.params;
  db.query(
    "SELECT * FROM fusions WHERE date >= ? AND date <= ?",
    [startDate, endDate],
    (err, results) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json(results);
    }
  );
});

app.get("/api/creations/:startDate/:endDate", (req, res) => {
  const { startDate, endDate } = req.params;
  db.query(
    "SELECT * FROM creations WHERE date >= ? AND date <= ?",
    [startDate, endDate],
    (err, results) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json(results);
    }
  );
});