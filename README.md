# Animetrix

A bot made for Pokemon TCG players, where people can collect, trade and battle with other players, made with [Discord.js](https://discord.js.org/)
and [MongoDB](https://www.mongodb.co) as the database.

<div align="left">
  <img alt="NPM Version" src="https://img.shields.io/npm/v/discord.js">
  <img alt="Node Current" src="https://img.shields.io/node/v/discord.js">
</div>

<br>

# Table of Contents
- [Animetrix](#animetrix)
- [Table of Contents](#table-of-contents)
- [How it works](#how-it-works)
  - [Static Database](#static-database) 
  - [Dynamic Database](#dynamic-database)
  - [App & API](#app--api)

# How it works

This bot uses two databases: **Static** & **Dynamic**

- ### Static Database
    This database stores the card informations got from Pokemon TCG API. As the name suggests, this is a static database which won't change constantly. This database is used to get any card information, etc. 

- ### Dynamic Database
    This database stores the user information like inventory, currency and other constantly changing data. This database is used to get and store user data. 

Both of the databases are stored in a free-tier mongodb cluster. 

## App & API

**App** is the nodejs application of the discord bot, while **API** is the nodejs application for providing API of the Static Datbase. Simply the **App** is connected to the dynamic database, whereas the **API** is connected to the static database. The **App** makes request to the **API** to fetch data from the static database and for user operations like creating user, updating user wallet, etc; the **App** will directly interact with the dynamic database. 

## Feedback 🗣️
If you encounter any issues, have suggestions for improvements, or want to report a bug, please feel free to [create an issue](https://github.com/StarReach/Animetrix/issues) on our GitHub repository. We value your feedback and will strive to enhance the application based on user input. 🤝

## Contributing 🤝
We welcome contributions from the open-source community. If you'd like to contribute to the development of this application, please follow our [contributing guidelines](CONTRIBUTING.md).

## License 📜
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏
- Special thanks to all our contributors for helping us create this project. 🌟
<p align="center">
  <img src="https://contributors-img.web.app/image?repo=StarReach/Animetrix" width=500 height=100/>

**Gotta Catch 'Em All!** 