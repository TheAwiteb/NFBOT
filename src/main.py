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
    DOTENV.get("NOTIFICATION_BOT_NAME", ""),
)
BOT = TeleBot(DOTENV.get("NOTIFICATION_BOT_TOKEN", None))


def notify_format(vars: dict, service: Services) -> str:
    """ Format notification

    Args:
        vars (dict): Notification variables
        service (Services): Notification service

    Raises:
        Exception: If the service unsupported
        TypeError: If service type not `Services`

    Returns:
        str: Notification context
    """
    if isinstance(service, Services):
        if service == Services.Twitter:
            template = DOTENV.get(
                "NOTIFICATION_BOT_TWITTER_TEMPLATE",
                "{TWEET_DESCRIPTION}\n\n> {TWITTER_LINK}",
            )
        elif service == Services.Instagram:
            template = DOTENV.get(
                "NOTIFICATION_BOT_INSTAGRAM_TEMPLATE",
                "{POST_DESCRIPTION}\n\n> {INSTAGRAM_LINK}",
            )
        else:
            raise Exception(f"`{service.name}` unsupported service")
    else:
        raise TypeError(
            f"`{service.__class__.__name__}` is invalid service type, should be `Services`"
        )
    for var, value in vars.items():
        template = template.replace(f"{{{var}}}", value)
    return template


def send_notification() -> None:
    last_tweet = BIBLIOGRAM_NITTER.last_nitter_post()
    last_post = BIBLIOGRAM_NITTER.last_bibliogram_post()
    chat_id = DOTENV.get("NOTIFICATION_BOT_TELEGRAM_CHAT_ID", None)

    if chat_id:
        if last_tweet and last_tweet != CONFIG.tweet:
            CONFIG.tweet = last_tweet
            tweet_variables = {
                "CHAT_ID": chat_id,
                "TWITTER_LINK": last_tweet.twitter_url.twitter,
                "NITTER_LINK": last_tweet.twitter_url.nitter,
                "TWEET_DESCRIPTION": last_tweet.description,
            }
            text = notify_format(tweet_variables, Services.Twitter)
            if last_tweet.medias:
                if "video" in last_tweet.medias[0]:
                    BOT.send_video(chat_id, last_tweet.medias[0], caption=text)
                else:
                    BOT.send_photo(chat_id, last_tweet.medias[0], caption=text)
            else:
                BOT.send_message(chat_id, text)

        if last_post and last_post != CONFIG.post:
            CONFIG.post = last_post
            post_variables = {
                "CHAT_ID": chat_id,
                "INSTAGRAM_LINK": last_post.insta_url.instagram,
                "BIBLIOGRAM_LINK": last_post.insta_url.bibliogram,
                "POST_DESCRIPTION": last_post.description,
            }
            text = notify_format(post_variables, Services.Instagram)
            if last_post.medias:
                if "video" in last_post.medias[0]:
                    BOT.send_video(chat_id, last_post.medias[0], caption=text)
                else:
                    BOT.send_photo(chat_id, last_post.medias[0], caption=text)
            else:
                BOT.send_message(chat_id, text)
    else:
        raise Exception("There is no chat_id")


def main() -> None:
    seconds = int(DOTENV.get("NOTIFICATION_BOT_DELAY", 120))
    while True:
        try:
            send_notification()
        except Exception as err:
            print(err)
        sleep(seconds)


if __name__ == "__main__":
    main()
