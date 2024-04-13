const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");

dotenv.config();

const app = express();

app.use(express.json());
app.use(cors({ 
  origin: "*"
}))

app.get("/", (req, res) => {
  res.status(200).json({ message: "Hello" });
});

app.listen(process.env.PORT, () => {
  console.log("listening on port " + process.env.PORT);
});
