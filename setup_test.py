from dotenv import load_dotenv
import os

load_dotenv()
print("API Key loaded:", os.getenv("GOOGLE_API_KEY") is not None)