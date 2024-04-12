const { SlashCommandBuilder } = require("discord.js");
const { getCardsThroughSet } = require("../../functions/migrateDB");
const CardModel = require("../../models/cardModel");

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

    await interaction.reply(`Migrating ${set}`);

    const res = await getCardsThroughSet(set);

    res.data.forEach(async (card) => {
      const newCard = new CardModel({
        
      });

      const card = await newCard.save();
    })
  },
};
