const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const mongoose = require("mongoose");

dotenv.config();

const app = express();

app.use(express.json());
app.use(cors({ 
  origin: "*"
}))

app.get("/", (req, res) => {
  res.status(200).json({ message: "Hello" });
});

mongoose.connect(process.env.MONGOURI).then(() => {
  console.log("Connected to MongoDB Successfully");
  app.listen(process.env.PORT, () => {
    console.log("Listening on port " + process.env.PORT);
  });
})
