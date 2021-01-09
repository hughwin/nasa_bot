from pathlib import Path

BASE_ADDRESS = "https://botsin.space/"
USERNAME = "@nasa_bot"
NASA_ADDRESS_IMAGES = "https://api.nasa.gov/planetary/apod?api_key=%s"
ROOT = Path(__file__).parent.parent
BASE_DIRECTORY = ROOT / "src"
DAILY_DIR = BASE_DIRECTORY / "daily"
DAILY_IMAGE = str(BASE_DIRECTORY / "daily" / "image.jpeg")