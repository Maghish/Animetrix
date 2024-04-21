const { SlashCommandBuilder } = require("discord.js");

var timeout = [];

module.exports = {
  data: new SlashCommandBuilder()
    .setName("daily")
    .setDescription("Claim daily rewards!"),
  async execute(interaction) {
    if (timeout.includes(interaction.user.id)) {
      return await interaction.reply({ content: "You are in a cooldown! Try again after 24 hours", ephemeral: true })
    }
    
    await interaction.reply("Hello!")

    timeout.push(interaction.user.id);
    setTimeout(() => {
      timeout.shift();
    }, 2400000)
  }
 }