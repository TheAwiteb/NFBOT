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

import os
import requests
from json import load, dump
from typing import List, Optional
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
        self.url = twitter_url
        self.description = description
        self.medias = medias

    def __repr__(self) -> str:
        return f"Tweet({', '.join(f'{key} = {val}' for key, val in self.__dict__.items())})"


class Post:
    def __init__(
        self, description: str, medias: Optional[List[str]], insta_url: InstaUrl
    ) -> None:
        self.url = insta_url
        self.description = description
        self.medias = medias

    def __repr__(self) -> str:
        return (
            f"Post({', '.join(f'{key} = {val}' for key, val in self.__dict__.items())})"
        )


class BibliogramNitter:
    def __init__(
        self,
        twitter_username: str,
        instagram_username: str,
        name: str,
        nitter_links: List[str] = NITTER_LINKS.copy(),
        bibliogram_links: List[str] = BIBLIOGRAM_LINKS.copy(),
    ) -> None:
        self.twitter_username = twitter_username
        self.instagram_username = instagram_username
        self.name = name
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

    def last_nitter_post(self) -> Tweet:
        """ Returns last tweet from username

        Returns:
            Tweet: The last tweet
        """
        content = self.nitter_page()
        tweets = content.soup.find("div", class_="timeline")
        for tweet in tweets.find_all("div", class_="timeline-item"):
            if tweet.find("div", class_="pinned"):
                continue
            break
        description = tweet.find("div", class_="tweet-content media-body").text
        link = tweet.find("a", class_="tweet-link")["href"]
        medias = list(
            map(lambda img: content.domain + img["src"], tweet.find_all("img")[1:])
        )

        return Tweet(
            description,
            medias or None,
            TwitterUrl(content.domain + link, "https://twitter.com" + link),
        )

    def last_bibliogram_post(self) -> Post:
        content = self.bibliogram_page()
        last_post = content.soup.find("a", class_="sized-link")
        link = last_post["href"]
        post = BeautifulSoup(requests.get(content.domain + link).content, "html.parser")
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


class Config:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.__last_tweet: Optional[TwitterUrl] = None
        self.__last_post: Optional[InstaUrl] = None

    def __update_json(self) -> None:
        """ Update json file
        """
        is_new = False
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                is_new = True

        with open(self.filename, "r") as f:
            json: dict = {} if is_new else load(f)
            json.update(
                {"tweet": self.__last_tweet.__dict__ if self.__last_tweet else None}
            )
            json.update(
                {"post": self.__last_post.__dict__ if self.__last_post else None}
            )

        with open(self.filename, "w") as f:
            dump(json, f)

    @property
    def tweet(self) -> Optional[TwitterUrl]:
        return self.__last_tweet

    @tweet.setter
    def tweet(self, tweet: TwitterUrl) -> None:
        self.__last_tweet = tweet
        self.__update_json()

    @property
    def post(self) -> Optional[InstaUrl]:
        return self.__last_post

    @post.setter
    def post(self, post: InstaUrl) -> None:
        self.__last_post = post
        self.__update_json()
