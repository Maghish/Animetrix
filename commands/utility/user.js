const { SlashCommandBuilder } = require("discord.js");

module.exports = {
  data: new SlashCommandBuilder().setName("1").setDescription("1"),

  async execute(interaction) {
    await interaction.reply("1");
  },
};
