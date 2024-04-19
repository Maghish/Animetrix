const MoneyModel = require("../models/money.model");

async function createUser(UID) {
  try {
    const userMoney = await MoneyModel.findOne({ UID: UID })
    if (userMoney) {
      return [false, "You can only use this command once!"]
    }

    else {
      const newUserMoney = new MoneyModel({ UID: UID, wallet: 0 });
      await newUserMoney.save();
      return [true, "You can now start your journey!"];
    }
    
    
  } catch (error) {
    console.error(error);
    return [false, "There was an unexpected error!"];
  }

   
}

module.exports = createUser;