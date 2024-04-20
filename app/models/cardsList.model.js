const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const cardListSchema = new Schema(
  {
    UID: { type: String, required: true },
    cards: [
      {
        id: { type: Number, required: true },
        name: { type: String, required: true },
        supertype: { type: String, required: true },
        subtypes: { type: [String], required: true },
        types: { type: [String], required: true },
        image: { type: String, required: true },
        rarity: { type: String, required: true },
      },
    ],
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("CardListModel", cardListSchema);
