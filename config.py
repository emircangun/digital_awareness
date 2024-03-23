from dotenv import load_dotenv
import os

PORT=8080
LOCALHOST_IP="localhost"

load_dotenv()

for key in os.environ:
    globals()[key] = os.getenv(key)