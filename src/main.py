# NFBOT (Notification Bot) - Is bot to send notification from twitter and instagram to telegram channel
#      Copyright (C) 2020-2022  <name of author>

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.

# You should have received a copy of the GNU Affero General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

# Also add information on how to contact you by electronic and paper mail.

# If your software can interact with users remotely through a computer network,
# you should also make sure that it provides a way for users to get its source.
# For example, if your program is a web application, its interface could display
# a "Source" link that leads users to an archive of the code.  There are many
# ways you could offer source, and different solutions will be better for different
# programs; see section 13 for the specific requirements.

# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary. For
# more information on this, and how to apply and follow the GNU AGPL, see <http://www.gnu.org/licenses/>.

from time import sleep
from utils import *
from telebot import TeleBot
from dotenv import load_dotenv
from os import environ

load_dotenv()
DOTENV = {**environ}
CONFIG = Config("lasts.json")
BIBLIOGRAM_NITTER = BibliogramNitter(
    DOTENV.get("NOTIFICATION_BOT_TWITTER_USERNAME", None),
    DOTENV.get("NOTIFICATION_BOT_INSTAGRAM_USERNAME", None),
    DOTENV.get("NOTIFICATION_BOT_NAME", None),
)
BOT = TeleBot(DOTENV.get("NOTIFICATION_BOT_TOKEN", None))


def send_notification() -> None:
    last_tweet = BIBLIOGRAM_NITTER.last_nitter_post()
    last_post = BIBLIOGRAM_NITTER.last_bibliogram_post()
    chat_id = DOTENV.get("NOTIFICATION_BOT_TELEGRAM_CHANNEL_ID", None)

    if last_tweet and last_tweet != CONFIG.tweet:
        CONFIG.tweet = last_tweet
        text = f"تغريدة جديدة من {BIBLIOGRAM_NITTER.name}:\n{last_tweet.description}\n\n> {last_tweet.twitter_url.twitter}"
        if last_tweet.medias:
            if "video" in last_tweet.medias[0]:
                BOT.send_video(chat_id, last_tweet.medias[0], caption=text)
            else:
                BOT.send_photo(chat_id, last_tweet.medias[0], caption=text)
        else:
            BOT.send_message(chat_id, text)

    if last_post != CONFIG.post:
        CONFIG.post = last_post
        text = f"منشور جديد من {BIBLIOGRAM_NITTER.name}:\n{last_post.description}\n\n> {last_post.insta_url.instagram}"
        if last_post.medias:
            if "video" in last_post.medias[0]:
                BOT.send_video(chat_id, last_post.medias[0], caption=text)
            else:
                BOT.send_photo(chat_id, last_post.medias[0], caption=text)
        else:
            BOT.send_message(chat_id, text)


def main() -> None:
    seconds = int(DOTENV.get("NOTIFICATION_BOT_DELAY", None))
    while True:
        try:
            send_notification()
        except Exception as err:
            print(err)
        sleep(seconds)


if __name__ == "__main__":
    main()
