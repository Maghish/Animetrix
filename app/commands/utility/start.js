const { SlashCommandBuilder, EmbedBuilder } = require("discord.js");
const createUser = require("../../functions/createUser");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("start")
    .setDescription("Start your journey!"),

  async execute(interaction) {
    try {
      await interaction.reply("Loading...");

      const result = await createUser(interaction.user.id.toString());

      await interaction.editReply(result[1]);
    } catch (error) {
      await interaction.reply("Error!");
    }
  },
};
