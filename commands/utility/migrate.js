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
      /* 
        Some of the fields in the Pokemon TCG API Card object might be presennt such as listed below.
        So all of the if condition blocks will check if the card object has that field and if so it will update the variables below,
        if there is no field in the card object, then it will be empty to be a placeholder in the Card Model.
      */
    
      let evolvesFrom = "";
      let evolvesTo = [];
      let rules = [];
      let abilities = [];
      let attacks = [];
      let weaknesses = [];
      let resistances = [];
      let retreatCost = [];
      let flavorText = [];

      if (card.evolvesFrom) {
        evolvesFrom = card.evolvesFrom;
      }

      if (card.evolvesTo) {
        evolvesTo = card.evolvesTo;
      }

      if (card.rules) {
        rules = card.rules;
      }

      if (card.abilities) {
        card.abilities.forEach((ability) => {
          abilities.push({
            name: ability.name,
            text: ability.text,
            type: ability.type,
            functionID: ""
          })  
        })
      }

      if (card.attacks) {
        card.attacks.forEach((move) => {
          attacks.push({
            name: move.name,
            text: move.text,
            damage: move.damage,
            cost: move.cost,
            functionID: ""
          })
        });
      }

      if (card.weaknesses) {
        weaknesses = card.weaknesses;
      }

      if (card.resistances) {
        resistances = card.resistances;
      }

      if (card.retreatCost) {
        retreatCost = card.retreatCost;
      }

      if (card.flavorText) {
        flavorText = card.flavorText;
      }

      const newCard = new CardModel({
        id: card.id,
        name: card.name,
        supertype: card.supertype,
        subtypes: card.subtypes,
        hp: card.hp,
        types: card.types,
        evolvesFrom: evolvesFrom,
        evolvesTo: evolvesTo,
        rules: rules,
        abilities: abilities,
        attacks: attacks,
        weaknesses: weaknesses,
        resistances: resistances,
        retreatCost: retreatCost,
        rarity: card.rarity,
        flavorText: card.flavorText,
        image: card.images.large
      });

      const savedCard = await newCard.save();
    });
  },
};
