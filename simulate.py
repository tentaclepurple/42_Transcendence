import time
import requests
from random import randint
from datetime import datetime, timedelta

N=100

MIN=1
MAX=10

def simulate_match():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NzM4MzUxLCJpYXQiOjE3MTk2ODMxMTQsImp0aSI6ImE5ZWRiOWUzNTIxZjQ5YzU5OThjNjlmNzdmZGQ0NDZhIiwidXNlcl9pZCI6M30.ZocIQ5D23aM2lsWpgbyAtXtBQ0HMUM_RWuvXhgySLeQ"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Cookie': 'sessionid=vra145hk2smcye3lwco61ti6x6ui63ql'
    }
    now = datetime.now()
    for idx in range(N):

        now += timedelta(minutes=idx)
        game_info = {
            "player1": 0,
            "player2": 0,
            "finished_at": now.isoformat(),
            "legit": True
        }

        player1 = randint(MIN, MAX)
        player2 = randint(MIN, MAX)
        while player1 == player2:
            player2 = randint(MIN, MAX)

        game_info["player1"] = player1
        game_info["player2"] = player2

        if randint(0,1):
            game_info["winner"] = game_info["player1"]
        else:
            game_info["winner"] = game_info["player2"]

        print(game_info)

        res = requests.post("http://localhost:8000/pong/games/simulate/", json=game_info, headers=headers)
        print(res.status_code)

def create_users():

    users = [
        {
            "username": "CaptainSparkle",
            "email": "captain@sparkle.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Sparkle"
        },
        {
            "username": "MysticMoonlight",
            "email": "mystic@moonlight.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Mystic"
        },
        {
            "username": "DaringDragon",
            "email": "daring@dragon.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Dragon"
        },
        {
            "username": "WhisperingWind",
            "email": "whispering@wind.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Whisper"
        },
        {
            "username": "StarlightStardust",
            "email": "starlight@stardust.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Starlight"
        },
        {
            "username": "SapphireSky",
            "email": "sapphire@sky.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Sapphire"
        },
        {
            "username": "GoldenGlimmer",
            "email": "golden@glimmer.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Golden"
        },
        {
            "username": "SilentStorm",
            "email": "silent@storm.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Silent"
        },
        {
            "username": "EchoingEmber",
            "email": "echoing@ember.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Ember"
        },
        {
            "username": "LuminousLagoon",
            "email": "luminous@lagoon.com",
            "password1": "popopo8787",
            "password2": "popopo8787",
            "nickname": "Lagoon"
        }
    ]

    headers = {
        "content-type": "application/json"
    }
    for user in users:

        res = requests.post("http://localhost:8000/auth/registration/", headers=headers, json=user)
        if res.ok:
            print(f"User: {user['username']} created successfully!!")
        else:
            print(f"Error: {res.status_code}")

def main() -> int:
    
    create_users()
    #simulate_match()


if __name__ == "__main__":
    main()