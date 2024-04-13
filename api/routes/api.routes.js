const express = require("express");
const { migrate } = require("../controllers/api.controller");

const router = express.Router();

router.post("/migrate", migrate)

module.exports = router;