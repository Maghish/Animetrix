const express = require("express");
const { migrate, getCard } = require("../controllers/api.controller");

const router = express.Router();

router.post("/migrate", migrate);
router.post("/getcard", getCard)

module.exports = router;