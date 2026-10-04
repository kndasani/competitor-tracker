import os
from dotenv import load_dotenv
from parallel import Parallel

load_dotenv()

api_key = os.getenv("PARALLEL_API_KEY")

if not api_key or api_key == "your_parallel_api_key_here":
    print("Error: PARALLEL_API_KEY is missing or unchanged in .env file.")
else:
    try:
        client = Parallel(api_key=api_key)
        print("Environment setup successful! Parallel SDK initialized successfully.")
    except Exception as e:
        print(f"Error initializing Parallel client: {e}")