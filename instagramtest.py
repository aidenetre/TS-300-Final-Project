0.
# instagram.py is the main file that will be run to post to Instagram
# author: @aidenetre

import os
from instagrapi import Client

# Log in to Instagram
def login_instagram(username, password):
    client = Client()
    client.login(username, password)
    return client

def main():
    # Set your Instagram username and password here
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    print(username)
    print(password)

    if not username or not password:
        print("Error: Instagram username or password not found.")
        return

if __name__ == "__main__":
    main()
