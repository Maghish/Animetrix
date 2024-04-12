const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const cardSchema = new Schema(
  {
    id: { type: String, required: true },
    name: { type: String, required: true },
    supertype: { type: String, required: true },
    subtypes: { type: [String], required: true },
    hp: { type: Number, required: true },
    types: { type: [String], required: true },
    evolvesFrom: { type: String, required: true },
    evolvesTo: { type: [String], required: true },
    rules: { type: [String], required: true },
    // ancientTrait
    abilities: { type: [], required: true },
    attacks: { type: [], required: true },
    weaknesses: { type: [], required: true },
    resistances: { type: [], required: true },
    retreatCost: { type: [String], required: true },
    // set
    rarity: { type: String, required: true },
    flavorText: { type: String, required: true },
    image: { type: String, required: true },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("CardModel", cardSchema);
