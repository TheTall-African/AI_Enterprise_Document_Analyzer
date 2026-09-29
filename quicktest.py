import os
from dotenv import load_dotenv

load_dotenv()

print("api here:", bool(os.getenv("OPENAI_API_KEY")))