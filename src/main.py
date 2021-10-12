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
    try:
        r = requests.get(settings.NASA_ADDRESS_IMAGES % os.getenv("NASA"))
        json = r.json()
        urllib.request.urlretrieve(json["url"], settings.DAILY_IMAGE) # There seems to be an issue caused by using
        # the "hdurl option that causes the bot to crash.
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
