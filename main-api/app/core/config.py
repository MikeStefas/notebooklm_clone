import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

secret: str = os.getenv("SECRET_KEY") or ""

ALGORITHM: str = os.getenv("ALGORITHM") or ""
REFRESH_secret: str = os.getenv("REFRESH_SECRET_KEY") or ""


