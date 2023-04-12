# file: testing.py
# author: @aidenetre
# description: This file contains current testing functions that will be run for development purposes only

#------------------------------------IMPORTS------------------------------------#
import os
import time
import itertools
from post import Post
from instagrapi import Client

# Log in to Instagram
def login_instagram():
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')

    if not username or not password:
        print("Error: Instagram username or password not found.")
        return

    client = Client()
    client.login(username, password)

    print("Logged in to Instagram")
    return client

# Post image and description on Instagram
def post_on_instagram(client, image_path, description):
    try:
        client.photo_upload(image_path, description)
        client.photo_upload_to_story(image_path, description)
        print(f"Posted image with description: {description}")
    except Exception as e:
        print(f"Error posting image and description: {e}")

def main():
    # Set the interval between posts (6 hours)
    interval = 15 * 60

    post_counter = itertools.count(start = 1)

    while True:
        try:  
            # Pass the 'is_educational' argument to the 'generate_post' function
            is_educational = next(post_counter) % 4 == 0
            post = Post(is_educational = is_educational)

            client = login_instagram()

            post = None

            if client != None:
                client = None

        except Exception as e:
            print(f"Error generating or posting: {e}")
        
        print("Start : %s" % time.ctime())
        time.sleep(interval)
        print("End : %s" % time.ctime())

if __name__ == "__main__":
    main()
