const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const invSchema = new Schema(
  {
    UID: { type: String, required: true },
    inventory: {
      packs: [
        {
          name: { type: String, required: true },
          amount: { type: Number, required: true }
        }
      ],
      chests: [
        {
          name: { type: String, required: true },
          amount: { type: Number, required: true },
          rarity: { type: String, required: true },
        }
      ]
    }
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("InvModel", invSchema);
