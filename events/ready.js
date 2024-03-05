const { Events } = require("discord.js");
const mongoose = require("mongoose");
const dotenv = require("dotenv");

dotenv.config();

const MONGOURI = process.env.MONGOURI;

module.exports = {
  name: Events.ClientReady,
  once: true,
  async execute(client) {
    console.log(`Ready! Logged in as ${client.user.tag}`);
    await mongoose.connect(MONGOURI);
    if (mongoose.connect) {
      console.log("Connected to MongoDB");
    }
  },
};
