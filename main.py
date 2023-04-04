# Author: @aidenetre

#--- IMPORTS ---#
import os
import openai
import requests
import re
from datetime import date
import time
from pathlib import Path

# Set up OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY") # Set your OpenAI API key here, retrieve from PATH

def generate_headline(): # Generates the fake news headline using the prompt as a prompt
    try:
        today = date.today() # Gets the current date
        base_fake_news_prompt = f"Generate a current financial news headline for the current date {today}:"
        response = openai.Completion.create(
            engine = "text-davinci-002",
            prompt = base_fake_news_prompt,
            max_tokens = 100,
            temperature = 0.7,
            top_p = 1,
        )
        fake_news_headline = response["choices"][0]["text"] # Extracts the fake news headline from the generated post
        return fake_news_headline # Returns the fake news headline
    except openai.error.OpenAIError as e:
        print(f"Error generating headline: {e}")
        return None

def generate_image_prompt(fake_news_headline): # Generates the image prompt using the headline as a prompt
    try:
        base_image_prompt = f"Write a sentence describing the image in an instagram post relating to the financial news headline: {fake_news_headline} using the following template: PROMPT: <A [format] of [scene] in the style of [style], [perspective].> You need to replace the parameters in the brackets. Use the following lists to choose from for each one: format: ... style: ... perspective: ... The scene parameter needs to specify an object or subject performing an action. Describe the scenery. Describe the mood and the lighting."
        response = openai.ChatCompletion.create( # Generates the image prompt using the headline as a prompt
            model = "gpt-3.5-turbo",
            messages = [{"role": "user", "content": base_image_prompt}],
            max_tokens = 100,
            temperature = 0.7,
            top_p = 1,
        )

        generated_image_prompt = response["choices"][0]["message"]["content"] # Extracts the image prompt from the generated post
        return generated_image_prompt # Returns the image prompt
    except openai.error.OpenAIError as e:
        print(f"Error generating image prompt: {e}")
        return None

def generate_post_description(fake_news_headline): # Generates the post description using the headline as a prompt
    try:
        description_prompt = f"Create an instagram post for the following financial news headline: {fake_news_headline} using the following template: DESCRIPTION: <description including hashtags and emojis.>"
        response = openai.ChatCompletion.create( # Generates the post description
            model = "gpt-3.5-turbo",
            messages = [{"role": "user", "content": description_prompt}],
            max_tokens = 100,
            temperature = 0.7,
            top_p = 1,
        )

        generated_post_description = response["choices"][0]["message"]["content"] # Extracts the post description from the generated post
        return generated_post_description # Returns the post description
    except openai.error.OpenAIError as e:
        print(f"Error generating post: {e}")
        return None

def generate_image(generated_image_prompt): # Generates the image using the image prompt as a prompt
    try:
        response = openai.Image.create(
            prompt = generated_image_prompt,
            num_images = 1,
        )

        image_url = response["data"][0]["url"] # Extracts the image URL from the generated post
        return image_url # Returns the image URL
    except openai.error.OpenAIError as e:
        print(f"Error generating image: {e}")
        return None
    
def extract_image_prompt(generated_image_prompt):
    try:
        # Find the index of "PROMPT: "
        prompt_index = generated_image_prompt.find("PROMPT: ") + len("PROMPT: ") # Finds the index of "PROMPT: "

        # Extract the prompt
        image_prompt = generated_image_prompt[prompt_index:].strip() # Removes the "PROMPT: " from the start of the prompt

        if image_prompt.startswith("nt"): # Removes the "nt" from the start of the prompt
            image_prompt = image_prompt[2:].strip()

        print("Image prompt: " + image_prompt) # Prints the image prompt to the console

        return image_prompt  # Returns the image prompt
    except Exception as e:
        print(f"Error extracting image prompt: {e}")
        return None

def extract_post_description(generated_post_description):
    try:
        # Find the index of "DESCRIPTION: "
        description_index = generated_post_description.find("DESCRIPTION: ") + len("DESCRIPTION: ") # Finds the index of "DESCRIPTION: "

        # Extract the description
        post_description = generated_post_description[description_index:].strip() # Removes the "DESCRIPTION: " from the start of the description

        if post_description.startswith("nt"): # Removes the "nt" from the start of the description
            image_prompt = image_prompt[2:].strip()

        print("Post description: " + post_description) # Prints the post description to the console

        return post_description  # Returns the post description
    except Exception as e:
        print(f"Error extracting post description: {e}")
        return None

def sanitize_filename(filename): # Sanitizes the filename
    # Remove newline characters
    filename = filename.replace("\n", " ")

    # Replace any characters that are not letters, numbers, or spaces with underscores
    return re.sub(r'[^\w\s]+', '_', filename) # Returns the sanitized filename

def save_post(fake_news_headline, image_prompt, image_url, post_description, output_dir="generated_posts"): # Saves the post and image to a text file and a jpg file respectively
    try:
        # Create a unique identifier based on the current time
        unique_id = int(time.time())
        output_path = Path(output_dir) / str(unique_id) # Creates a path to the output directory with a unique subdirectory
        output_path.mkdir(parents=True, exist_ok=True) # Creates the output directory if it doesn't exist

        # Sanitize headline for use in file name
        sanitized_headline = sanitize_filename(fake_news_headline)

        # Save post and description to text file
        post_filename = output_path / f"{sanitized_headline[:10]}_post.txt"
        with open(post_filename, "w", encoding="utf-8") as post_file:
            post_file.write(f"Headline: {fake_news_headline}\n\n") # Writes the headline to the text file
            post_file.write(f"Image Prompt: {image_prompt}\n\n") # Writes the image prompt to the text file
            post_file.write(f"Image URL: {image_url}\n\n") # Writes the image URL to the text file
            post_file.write(f"Description: {post_description}\n\n") # Writes the description to the text file

        # Save image to file
        image_response = requests.get(image_url) # Gets the image from the URL
        image_filename = output_path / f"{sanitized_headline[:10]}_image.jpg" # Creates the image filename
        with open(image_filename, "wb") as image_file:
            image_file.write(image_response.content) # Writes the image to the image file

        print(f"Post and image saved to {output_path}") # Prints the path and save confirmation to the output directory
    except Exception as e:
        print(f"Error saving post and image: {e}")

def main(): # Main function
    fake_news_headline = generate_headline() # Generates the fake news headline
    if fake_news_headline is None:
        print("Failed to generate headline. Exiting.")
        return

    generated_image_prompt = generate_image_prompt(fake_news_headline) # Generates the image prompt
    if generated_image_prompt is None:
        print("Failed to generate image prompt. Exiting.")
        return
    image_prompt = extract_image_prompt(generated_image_prompt)  # Extracts the image prompt

    generated_post_description = generate_post_description(fake_news_headline) # Generates the post description
    if generated_post_description is None:
        print("Failed to generate post description. Exiting.")
        return
    post_description = extract_post_description(generated_post_description)  # Extracts the post description

    image_url = generate_image(image_prompt) # Generates the image using the image prompt as a prompt
    if image_url is None:
        print("Failed to generate image. Exiting.")
        return

    save_post(fake_news_headline, image_prompt, image_url, post_description) # Saves the post and image to a text file and a jpg

if __name__ == "__main__": # Runs the main function
    main()
