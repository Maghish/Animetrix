const { SlashCommandBuilder } = require("discord.js");
const { EmbedBuilder } = require("discord.js");
const axios = require("axios");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("find")
    .setDescription("Find a pokemon card")
    .addStringOption((option) =>
      option
        .setName("pokemon")
        .setDescription("Enter a pokemon name to search")
        .setRequired(true)
    ),

  async execute(interaction) {
    const cardName = interaction.options.getString("pokemon");

    try {
      const APIURL = `${process.env.APIURL}api/getcard`;
      const res = await axios.post(APIURL, {
        cardName: cardName,
      });

      const embed = new EmbedBuilder()
        .setTitle(res.data.card[0].name)
        .setImage(res.data.card[0].image);

      await interaction.reply({ embeds: [embed] });
    } catch (error) {
      await interaction.reply("Error!");
      console.error(error);
    }
  },
};
