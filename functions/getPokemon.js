const pokemon = require("pokemontcgsdk");

pokemon.configure({ apiKey: "761784d9-5af8-4409-949d-ba4f9e8f5c52 " });

function GetPokemon(pokemonID) {
  pokemon.card.find(pokemonID).then((card) => {
    console.log(card.images.large);
  });
}

GetPokemon("base1-4");
