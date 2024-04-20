const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const decksListSchema = new Schema(
  {
    UID: { type: String, required: true },
    decks: [
      {
        id: { type: Number, required: true },
        name: { type: String, required: true },
        description: { type: String, required: false, default: "" },
        cards: { type: [Number], required: true }
      }
    ]
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("DecksListModel", decksListSchema);
