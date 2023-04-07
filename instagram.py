# instagram.py is the main file that will be run to post to Instagram
# author: @aidenetre

import os
import time
from instagrapi import Client
from post import generate_post

# Log in to Instagram
def login_instagram(username, password):
    client = Client()
    client.login(username, password)
    return client

# Post image and description on Instagram
def post_on_instagram(client, image_path, description):
    try:
        client.photo_upload_to_story(image_path, description)
        print(f"Posted image with description: {description}")
    except Exception as e:
        print(f"Error posting image and description: {e}")

def main():
    # Set your Instagram username and password here
    username = os.environ.get('INSTAGRAM_USERNAME')
    password = os.environ.get('INSTAGRAM_PASSWORD')

    if not username or not password:
        print("Error: Instagram username or password not found.")
        return

    client = login_instagram(username, password)

    # Set the interval between posts (6 hours)
    interval = 6 * 60 * 60

    while True:
        try:
            # Generate a post using the existing generate_post function
            post = generate_post()

            # Post the image and description on Instagram
            post_on_instagram(client, post.image_path, post.post_description)

        except Exception as e:
            print(f"Error generating or posting: {e}")

        # Wait for the specified interval before generating the next post
        time.sleep(interval)

if __name__ == "__main__":
    main()
