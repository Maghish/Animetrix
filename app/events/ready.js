const { Events } = require("discord.js");
const mongoose = require("mongoose");
const dotenv = require("dotenv");
const { PermissionsBitField } = require('discord.js');

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
    setInterval(() => {
      client.guilds.cache.forEach((guild) => {
        // Get an array of text channels where the bot can send messages
        const textChannels = guild.channels.cache
          .filter(
            (channel) =>
              channel.type === 0 &&
              channel
                .permissionsFor(client.user)
                .has(PermissionsBitField.Flags.SendMessages)
          )
          .map((channel) => channel);

        // Select a random channel
        if (textChannels.length > 0) {
          const randomIndex = Math.floor(Math.random() * textChannels.length);
          const randomChannel = textChannels[randomIndex];
          randomChannel.send("hi").catch(console.error);
        }
      });
    }, 60000); // Repeat every minute
  },
};
