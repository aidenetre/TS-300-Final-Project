# instagram.py is the main file that will be run to post to Instagram
# author: @aidenetre

import os
import time
import itertools
from post import Post
from instagrapi import Client

# Log in to Instagram
def login_instagram():
    # Set your Instagram username and password here
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')

    if not username or not password:
        print("Error: Instagram username or password not found.")
        return

    client = Client()
    client.login(username, password)
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
    interval = 60 * 60

    post_counter = itertools.count(start = 4)

    while True:

        client = login_instagram()

        try:
            # Pass the 'is_educational' argument to the 'generate_post' function
            is_educational = next(post_counter) % 4 == 0
            post = Post(is_educational = is_educational)

            # Post the image and description on Instagram
            post_on_instagram(client, post.image_path, post.post_description)

        except Exception as e:
            print(f"Error generating or posting: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    main()
