from dotenv import load_dotenv
import os

load_dotenv()

for key in os.environ:
    globals()[key] = os.getenv(key)