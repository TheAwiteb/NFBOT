<div align="center">
  <h1>NFBOT (Notification Bot)</h1>
  Telegram bot to send notification from twitter and instagram to telegram chat/group/channel
</div>

## Requirements
* [Python+3.8](https://python.org/)

## Environment Variables

|                 Name                |                                             Description                                  | Is Required |                   Default                   |
|:-----------------------------------:|:----------------------------------------------------------------------------------------:|:-----------:|:-------------------------------------------:|
|`NOTIFICATION_BOT_TWITTER_TEMPLATE`  |Twitter notification template. see [Twitter Variables](#twitter-template-variables)       |No           |`"{TWEET_DESCRIPTION}\n\n> {TWITTER_LINK}"`  |
|`NOTIFICATION_BOT_INSTAGRAM_TEMPLATE`|Instagram notification template. see [Instagram Variables](#instagram-template-variables) |No           |`"{POST_DESCRIPTION}\n\n> {INSTAGRAM_LINK}"` |
|`NOTIFICATION_BOT_TWITTER_USERNAME`  |Twitter username                                                                          |No           | -                                           |
|`NOTIFICATION_BOT_INSTAGRAM_USERNAME`|Instagram username                                                                        |No           | -                                           |
|`NOTIFICATION_BOT_TELEGRAM_CHAT_ID`  |Telegram chat/group/channel ID [@MyIdBot]                                                 |Yes          | -                                           |
|`NOTIFICATION_BOT_TOKEN`             |Telegram bot token [@BotFather]                                                           |Yes          | -                                           |
|`NOTIFICATION_BOT_DELAY`             |The time between each new post check ( in seconds )                                       |No           |120s                                         |

[@MyIdBot]: https://t.me/myidbot
[@BotFather]: https://t.me/botfather

## Templates
With template you can customization notification as you want
> Note: Put the variable name in the template in curly brackets `{}`

### Twitter Template Variables

|        Name        |                        Description                         |
|:------------------:|:----------------------------------------------------------:|
|`CHAT_ID`           | The ID of the chat to which this notification will be sent |
|`TWITTER_LINK`      | Tweet link on [Twitter]                                    |
|`NITTER_LINK`       | Tweet link on [Nitter] service                             |
|`TWEET_DESCRIPTION` | Tweet description                                          |

[Twitter]: https://twitter.com
[Nitter]: https://nitter.net

### Instagram Template Variables

|        Name       |                        Description                         |
|:-----------------:|:----------------------------------------------------------:|
|`CHAT_ID`          | The ID of the chat to which this notification will be sent |
|`INSTAGRAM_LINK`   | Tweet link on [Instagram]                                  |
|`BIBLIOGRAM_LINK`  | Tweet link on [Bibliogram] service                         |
|`POST_DESCRIPTION` | Tweet description                                          |

[Instagram]: https://instagram.com
[Bibliogram]: https://bibliogram.art

## Bot interface
Rename [`.env.example`](.env.example) to `.env`, and fill the [variables](#environment-variables), and the bot will send the notification in the channel

## Installation
### Building
You must fill the variables in environment file (`.env`)

#### Install Requirements
```bash
pip3 install -r requirements.txt
```

### Running
```bash
python3 ./src/main.py
```

## License
The [GNU Affero General Public](https://www.gnu.org/licenses/agpl-3.0.en.html) License is a free, copyleft license for software and other kinds of works, specifically designed to ensure cooperation with the community in the case of network server software.
