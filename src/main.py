import time

import schedule as schedule
from mastodon import Mastodon
from datetime import date
import os
import requests
import urllib

from src import settings

mastodon = Mastodon(
    access_token=os.getenv("ACCESS_TOKEN"),
    api_base_url=settings.BASE_ADDRESS
)


def main():
    os.makedirs(str(settings.DAILY_DIR), exist_ok=True)
    schedule.every().day.at("10:30").do(toot_image_of_the_day)
    while True:
        schedule.run_pending()
        print("Thinking...")
        time.sleep(2)


def toot_image_of_the_day():
    """Method to toot a daily picture of the universe.

    This function exists to toot a picture of the universe to the instance the bot is running on. This is done to
    advertise the bot and to give users who are using the bot (maybe for the first time) the confidence that the bot
    is still running.
    """
    try:
        r = requests.get(settings.NASA_ADDRESS_IMAGES % os.getenv("NASA"))
        json = r.json()
        urllib.request.urlretrieve(json["hdurl"], settings.DAILY_IMAGE)
        description = json["title"]
        image_dict = mastodon.media_post(settings.DAILY_IMAGE, description=description)
        print(image_dict)
        today = date.today()
        message = today.strftime("%d/%m/%Y") + ": " + description
        mastodon.status_post(status=message, media_ids=image_dict)
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ == "__main__":
    main()
