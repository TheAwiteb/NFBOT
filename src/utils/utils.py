# NFBOT (Notification Bot) - Telegram bot to send notification from twitter and instagram to telegram chat/group/channel
#      Copyright (C) 2020-2022  TheAwiteb

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

import os
import requests
from json import load, dump
from typing import Any, List, Optional, Union
from enum import Enum, auto
from bs4 import BeautifulSoup

__all__ = (
    "NITTER_LINKS",
    "BIBLIOGRAM_LINKS",
    "TwitterUrl",
    "InstaUrl",
    "Content",
    "Tweet",
    "Post",
    "BibliogramNitter",
    "Config",
    "Services",
)

NITTER_LINKS = [
    "https://nitter.net",
    "https://nitter.42l.fr",
    "https://nitter.pussthecat.org",
]

BIBLIOGRAM_LINKS = [
    "https://bibliogram.art",
    "https://bibliogram.pussthecat.org",
    "https://bibliogram.froth.zone",
]


class TwitterUrl:
    def __init__(self, nitter: str, twitter: str) -> None:
        self.nitter = nitter
        self.twitter = twitter

    def __eq__(self, other: "TwitterUrl") -> bool:
        return (
            other.__class__ == TwitterUrl
            and self.twitter == other.twitter
            and self.nitter == other.nitter
        )

    def __repr__(self) -> str:
        return f"TwitterUrl({', '.join(f'{key} = {val}' for key, val in self.__dict__.items())})"


class InstaUrl:
    def __init__(self, bibliogram: str, instagram: str) -> None:
        self.bibliogram = bibliogram
        self.instagram = instagram

    def __eq__(self, other: "InstaUrl") -> bool:
        return (
            other.__class__ == InstaUrl
            and self.instagram == other.instagram
            and self.bibliogram == other.bibliogram
        )

    def __repr__(self) -> str:
        return f"InstaUrl({', '.join(f'{key} = {val}' for key, val in self.__dict__.items())})"


class Content:
    def __init__(self, soup: BeautifulSoup, domain: str) -> None:
        self.domain = domain
        self.soup = soup

    def __repr__(self) -> str:
        return f"Content({', '.join(f'{key} = {val}' for key, val in self.__dict__.items())})"


class Tweet:
    def __init__(
        self, description: str, medias: Optional[List[str]], twitter_url: TwitterUrl
    ) -> None:
        self.twitter_url = (
            twitter_url
            if type(twitter_url) == TwitterUrl
            else TwitterUrl(**twitter_url)
        )
        self.description = description
        self.medias = medias

    def __members(self) -> List[Any]:
        return [self.twitter_url, self.description, self.medias]

    def __eq__(self, other: Any) -> bool:
        """ Return True if any 

        Args:
            other (Any): Other object

        Returns:
            bool: True if any 
        """
        if isinstance(other, Tweet):
            return any(
                map(
                    lambda objs: objs[0] == objs[1],
                    zip(self.__members(), other.__members()),
                )
            )
        return False

    def dict(self) -> dict:
        return {
            "description": self.description,
            "medias": self.medias,
            "twitter_url": self.twitter_url.__dict__,
        }

    def __repr__(self) -> str:
        return (
            f"Tweet({', '.join(f'{key} = {val}' for key, val in self.dict().items())})"
        )


class Post:
    def __init__(
        self, description: str, medias: Optional[List[str]], insta_url: InstaUrl
    ) -> None:
        self.insta_url = (
            insta_url if type(insta_url) == InstaUrl else InstaUrl(**insta_url)
        )
        self.description = description
        self.medias = medias

    def __members(self) -> List[Any]:
        return [self.insta_url, self.description, self.medias]

    def __eq__(self, other: Any) -> bool:
        """ Return True if any 

        Args:
            other (Any): Other object

        Returns:
            bool: True if any 
        """
        if isinstance(other, Post):
            return any(
                map(
                    lambda objs: objs[0] == objs[1],
                    zip(self.__members(), other.__members()),
                )
            )
        return False

    def dict(self) -> dict:
        return {
            "description": self.description,
            "medias": self.medias,
            "insta_url": self.insta_url.__dict__,
        }

    def __repr__(self) -> str:
        return (
            f"Post({', '.join(f'{key} = {val}' for key, val in self.dict().items())})"
        )


class BibliogramNitter:
    def __init__(
        self,
        twitter_username: Optional[str],
        instagram_username: Optional[str],
        nitter_links: List[str] = NITTER_LINKS.copy(),
        bibliogram_links: List[str] = BIBLIOGRAM_LINKS.copy(),
    ) -> None:
        self.twitter_username = twitter_username
        self.instagram_username = instagram_username
        self.nitter_links = nitter_links
        self.bibliogram_links = bibliogram_links

    def nitter_page(self) -> Content:
        """ Returns Nitter page of username

        Raises:
            Exception: Raise if all Nitter url are down

        Returns:
            Content: Nitter username content
        """
        for url in self.nitter_links:
            res = requests.get(f"{url}/{self.twitter_username}")
            if res.status_code == 200:
                break
            elif res.status_code == 404:
                raise Exception(f"'{self.twitter_username}' not found")
        else:
            raise Exception("All Nitter url are down")
        return Content(BeautifulSoup(res.content, "html.parser"), url)

    def bibliogram_page(self) -> Content:
        """ Returns Bibliogram page of username

        Raises:
            Exception: Raise if all Bibliogram url are down

        Returns:
            Content: Bibliogram username content
        """
        for url in self.bibliogram_links:
            res = requests.get(f"{url}/u/{self.instagram_username}")
            if res.status_code == 200:
                break
            elif res.status_code == 404:
                raise Exception(f"'{self.instagram_username}' not found")
        else:
            raise Exception("All Bibliogram url are down")
        return Content(BeautifulSoup(res.content, "html.parser"), url)

    def last_nitter_post(self) -> Optional[Tweet]:
        """ Returns last tweet from username

        Returns:
            Tweet: The last tweet
        """
        if self.twitter_username:  # else return None
            content = self.nitter_page()
            tweets = content.soup.find("div", class_="timeline")
            if tweets:  # else return None
                for tweet in tweets.find_all("div", class_="timeline-item") or []:
                    if tweet.find("div", class_="pinned"):
                        continue
                    break
                else:
                    return None
                description = tweet.find("div", class_="tweet-content media-body").text
                link = tweet.find("a", class_="tweet-link")
                if link:  # else return None
                    medias = list(
                        map(
                            lambda img: content.domain + img["src"],
                            tweet.find_all("img")[1:],
                        )
                    )
                    return Tweet(
                        description,
                        medias or None,
                        TwitterUrl(
                            content.domain + link["href"],
                            "https://twitter.com" + link["href"],
                        ),
                    )

    def last_bibliogram_post(self) -> Optional[Post]:
        if self.instagram_username:  # else return None
            content = self.bibliogram_page()
            last_post = content.soup.find("a", class_="sized-link")
            link = last_post["href"] if last_post else None
            if link:  # else return None
                post = BeautifulSoup(
                    requests.get(content.domain + link).content, "html.parser"
                )
                description = post.find(class_="structured-text description").text
                medias = list(
                    map(
                        lambda img: content.domain + img["src"],
                        post.find_all(class_="sized-image")
                        or post.find_all(class_="sized-video"),
                    )
                )
                return Post(
                    description,
                    medias,
                    InstaUrl(content.domain + link, "https://instagram.com" + link),
                )

    def __repr__(self) -> str:
        return f"BibliogramNitter({', '.join(f'{key} = {val}' for key, val in self.__dict__.items())})"


class Services(Enum):
    Twitter = auto()
    Instagram = auto()


class Config:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.__last_tweet: Optional[Tweet] = None
        self.__last_post: Optional[Post] = None

    def __read_json(self) -> dict:
        """ Read json file

        Returns:
            dict: Json
        """
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                dump({}, f)
        with open(self.filename, "r") as f:
            return load(f)

    def __write_json(self, json: dict) -> None:
        """ Write json in file

        Args:
            json (dict): Json to write it
        """
        with open(self.filename, "w") as f:
            dump(json, f)

    def __update_json(self) -> None:
        """ Update json file
        """
        json = self.__read_json()
        json.update({"tweet": self.__last_tweet.dict() if self.__last_tweet else None})
        json.update({"post": self.__last_post.dict() if self.__last_post else None})
        self.__write_json(json)

    def get_key(self, key: Services) -> Optional[Union[Tweet, Post]]:
        """ Return Url object from json, if is exists

        Args:
            key (Services): The Url you want

        Raises:
            TypeError: if key not 'Services'

        Returns:
            Optional[Union[Tweet, Post]]: Tweet or Post if exists
        """
        if key.__class__ == Services:
            json = self.__read_json()
            if json:
                tweet = json.get("tweet")
                post = json.get("post")
                self.__last_tweet = Tweet(**tweet) if tweet else None
                self.__last_post = Post(**post) if post else None
                return (
                    self.__last_tweet if key is Services.Twitter else self.__last_post
                )
            else:
                return None
        else:
            raise TypeError(f"'{key.__class__}' invalid key type, should be 'Services'")

    @property
    def tweet(self) -> Optional[Tweet]:
        return self.get_key(Services.Twitter)

    @tweet.setter
    def tweet(self, tweet: Tweet) -> None:
        self.get_key(Services.Twitter)  # load old values
        self.__last_tweet = tweet
        self.__update_json()

    @property
    def post(self) -> Optional[Post]:
        return self.get_key(Services.Instagram)

    @post.setter
    def post(self, post: Post) -> None:
        self.get_key(Services.Instagram)  # load old values
        self.__last_post = post
        self.__update_json()
