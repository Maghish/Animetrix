const { SlashCommandBuilder } = require("discord.js");
const { getCardsThroughSet } = require("../../functions/migrateDB");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("migrate")
    .setDescription("Migrates Pokemon TCG API sets to static database")
    .addStringOption((option) =>
      option
        .setName("set")
        .setDescription("Set to migrate cards from.")
        .setRequired(true)
    ),

  async execute(interaction) {
    const set = interaction.options.getString("set");

    const res = await getCardsThroughSet(set);
    console.log(res.data.length);

    await interaction.reply(`Migrating ${res.data[0].name}`);
  },
};
