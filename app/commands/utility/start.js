const { SlashCommandBuilder, EmbedBuilder } = require("discord.js");
const createUser = require("../../functions/createUser");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("start")
    .setDescription("Start your journey!"),

  async execute(interaction) {
    try {
      await createUser();
      await interaction.reply("Creating user...." + interaction.user);
    } catch (error) {
      await interaction.reply("Error!");
    }
  },
};
