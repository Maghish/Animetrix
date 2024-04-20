const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const moneyModel = new Schema(
  {
    UID: { type: String, required: true },
    wallet: { type: Number, required: true } 
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("MoneyModel", moneyModel);
