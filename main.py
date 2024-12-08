from flask import Flask
import requests
import os
from dot import load_dotenv

app = Flask(__name__)

load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")
