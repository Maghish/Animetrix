const MoneyModel = require("../models/money.model");
const CardListModel = require("../models/cardsList.model");
const InvModel = require("../models/inv.model");

async function createUser(UID) {
  try {
    const userMoney = await MoneyModel.findOne({ UID: UID });
    const userCardList = await CardListModel.findOne({ UID: UID });
    const userInv = await InvModel.findOne({ UID: UID });

    if (userMoney && userCardList) {
      return [false, "You can only use this command once!"];
    } else {
      const newUserMoney = new MoneyModel({ UID: UID, wallet: 0 });
      const newUserCardList = new CardListModel({
        UID: UID,
        cards: [
          // {
          //   id: 1,
          //   name: "Charizard",
          //   supertype: "Pokemon",
          //   subtypes: ["Stage 2"],
          //   types: ["Fire"],
          //   rarity: "Common",
          //   image: "https://images.pokemontcg.io/base1/4_hires.png",
          // },
        ],
      });
      const newUserInv = new InvModel({
        UID: UID,
        inventory: {
          pack: [
            // { name: "Pack1", amount: 8 }
          ],
          chests: [
            // { name: "Chest1", amount: 3, rarity: "Common" },
            // { name: "Chest2", amount: 1, rarity: "Ultra Rare" },
          ],
        },
      });
      await newUserMoney.save();
      await newUserCardList.save();
      await newUserInv.save();
      return [true, "You can now start your journey!"];
    }
  } catch (error) {
    console.error(error);
    return [false, "There was an unexpected error!"];
  }
}

module.exports = createUser;
