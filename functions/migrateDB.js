const pokemon = require("pokemontcgsdk");
const dotenv = require("dotenv");

dotenv.config();

pokemon.configure({ apiKey: `${process.env.POKEAPIKEY}` });

async function getCardsThroughSet(setName) {
  try {
    const cards = await pokemon.card.where({
      q: `set.name:${setName}`,
      pageSize: 10,
      page: 1
    });
    return cards;
  } catch (error) {
    return false;
  }
}

module.exports = {
  getCardsThroughSet,
};
