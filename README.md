# chunzie-bot
Telegram bot that connects to Plex

## Usage
This bot can be used in a private chat (with just the bot) or in a group. It can parse group messages so the command can be placed either before or after the bot is tagged.

`/scan` - This command connects to the Plex server and starts a conversation. It grabs the existing libraries in your Plex account and prompts you to select which library to scan. Once selected, the bot pushes the scan command to Plex.

`/cancel` - To be used after an initial `/scan` command to stop the conversation.

## Installation
The intended use case for this project is to be used in a [docker container](https://hub.docker.com/repository/docker/chunzie/chunzie-bot). It requires several environment variables as well as a `/config/whitelist` file to exist. The `whitelist` file is a text file with no extension that includes at least one Telegram chat id that can use the bot.

### Environment variables
**BOT_TOKEN** - Your Telegram bot API token.

**WEBHOOK_URL** - This bot runs on webhooks. See the [Telegram bot api documentation](https://core.telegram.org/bots/api#setwebhook) for instructions on how to set the webhook.

**PLEX_URL** - The URL of your Plex server (port included). e.g. http://localhost:34200

**PLEX_TOKEN** - The API token for your Plex server.
