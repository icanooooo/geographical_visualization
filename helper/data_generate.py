import requests
import random
import pytz

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def generate_person():
    response = requests.get('https://randomuser.me/api/?nat=CH')

    if response.status_code == 200:
        user_data = response.json()['results'][0]

        return user_data
    
    else:
        return f"error: {response.text}"
    