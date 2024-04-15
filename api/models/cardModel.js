const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const cardSchema = new Schema(
  {
    id: { type: String, required: false },
    name: { type: String, required: false },
    supertype: { type: String, required: false },
    subtypes: { type: [String], required: false },
    hp: { type: Number, required: false },
    types: { type: [String], required: false },
    evolvesFrom: { type: String, required: false, default: "" },
    evolvesTo: { type: [String], required: false, default: [] },
    rules: { type: [String], required: false, default: [] },
    // ancientTrait
    abilities: { type: [], required: false, default: [] },
    attacks: { type: [], required: false, default: []  },
    weaknesses: { type: [], required: false, default: [] },
    resistances: { type: [], required: false, default: [] },
    retreatCost: { type: [String], required: false, default: [] },
    // set
    rarity: { type: String, required: false },
    flavorText: { type: String, required: false, default: "" },
    image: { type: String, required: false },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("CardModel", cardSchema);
