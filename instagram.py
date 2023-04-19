# file: instagram.py
# author: @aidenetre
# description: This file contains the main function that will be run to post to Instagram

#------------------------------------IMPORTS------------------------------------#
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

    # Log in to Instagram
    client = Client()
    client.login(username, password)
    return client # Return the client object

# Post image and description on Instagram
def post_on_instagram(client, image_path, description):
    try: # Try to post the image and description
        client.photo_upload(image_path, description)
        client.photo_upload_to_story(image_path, description)
        print(f"Posted image with description: {description}")
    except Exception as e: # Catch any errors
        print(f"Error posting image and description: {e}")
 
# Main function
def main():
    # Set the interval between posts (4 hours)
    interval = 4 * 60 * 60

    # Create a counter to keep track of the number of posts between educational posts
    post_counter = itertools.count(start = 4)

    while True:
        try:  
            # Pass the 'is_educational' argument to the 'generate_post' function
            is_educational = next(post_counter) % 4 == 0 # Every 4 posts will be educational
            post = Post(is_educational = is_educational) # Generate a post

            # Log in to Instagram
            client = login_instagram()

            # Post the image and description on Instagram
            post_on_instagram(client, post.image_path, post.post_description)

            # Delete the post
            if post != None:
                post = None

            # Log out of Instagram
            if client != None:
                client = None

        # Catch any errors
        except Exception as e:
            print(f"Error generating or posting: {e}")
        
        print("Start : %s" % time.ctime()) # Print the start time
        time.sleep(interval) # Wait for the interval to pass
        print("End : %s" % time.ctime()) # Print the end time

# Run the main function
if __name__ == "__main__":
    main()
