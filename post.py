# File: post.py
# Author: @aidenetre

#--- IMPORTS ---#
import os
import openai
import requests
import re
import io
from PIL import Image, ImageDraw, ImageFont
from datetime import date
import time
from pathlib import Path

# Set up OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY") # Set your OpenAI API key here, retrieve from PATH

class Post:
    def __init__(self, generated_news_headline, generated_image_prompt, generated_post_description, image_url):
        self.generated_news_headline = generated_news_headline
        self.generated_image_prompt = generated_image_prompt
        self.generated_post_description = generated_post_description
        self.image_url = image_url
        self.news_headline = None
        self.image_prompt = None
        self.post_description = None

    def generate_headline(self): # Generates the fake news headline using the prompt as a prompt
        try:
            today = date.today() # Gets the current date
            base_news_prompt = f"Generate a current financial news headline for the current date {today}:"
            response = openai.Completion.create(
                engine = "text-davinci-002",
                prompt = base_news_prompt,
                max_tokens = 100,
                temperature = 0.7,
                top_p = 1,
            )
            self.generated_news_headline = response["choices"][0]["text"] # Extracts the fake news headline from the generated post
        except openai.error.OpenAIError as e:
            print(f"Error generating headline: {e}")
            self.generated_news_headline = None

    def generate_image_prompt(self): # Generates the image prompt using the headline as a prompt
        try:
            base_image_prompt = f"Write a sentence describing the image in an instagram post relating to the financial news headline: {self.news_headline} using the following template: PROMPT: <A [format] of [scene] in the style of [style], [perspective].> You need to replace the parameters in the brackets. Use the following lists to choose from for each one: format: ... style: ... perspective: ... The scene parameter needs to specify an object or subject performing an action. Describe the scenery. Describe the mood and the lighting."
            response = openai.ChatCompletion.create( # Generates the image prompt using the headline as a prompt
                model = "gpt-3.5-turbo",
                messages = [{"role": "user", "content": base_image_prompt}],
                max_tokens = 200,
                temperature = 0.7,
                top_p = 1,
            )

            self.generated_image_prompt = response["choices"][0]["message"]["content"] # Extracts the image prompt from the generated post
        except openai.error.OpenAIError as e:
            print(f"Error generating image prompt: {e}")
            self.generated_image_prompt = None

    def generate_post_description(self): # Generates the post description using the headline as a prompt
        try:
            description_prompt = f"Create an instagram post for the following financial news headline: {self.news_headline} using the following template: DESCRIPTION: <description including hashtags and emojis.>"
            response = openai.ChatCompletion.create( # Generates the post description
                model = "gpt-3.5-turbo",
                messages = [{"role": "user", "content": description_prompt}],
                max_tokens = 200,
                temperature = 0.7,
                top_p = 1,
            )

            self.generated_post_description = response["choices"][0]["message"]["content"] # Extracts the post description from the generated post
        except openai.error.OpenAIError as e:
            print(f"Error generating post: {e}")
            self.generated_post_description = None

    def generate_image(self): # Generates the image using the image prompt as a prompt
        try:
            response = openai.Image.create(
                prompt = self.image_prompt,
                num_images = 1,
            )

            self.image_url = response["data"][0]["url"] # Extracts the image URL from the generated post
        except openai.error.OpenAIError as e:
            print(f"Error generating image: {e}")
            self.image_url = None
    
    @staticmethod
    def extract_headline(generated_headline):
        if generated_headline.startswith("nt"): # Removes the "nt" from the start of the headline
            generated_headline = generated_headline[2:].strip()
        return generated_headline # Returns the headline

    @staticmethod
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

    @staticmethod
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
        
    def sanitize_filename(self, filename):
        filename = filename.replace("\n", " ")
        return re.sub(r'[^\w\s]+', '_', filename)

    def resize_image(self, image, size):
        return image.resize(size, Image.ANTIALIAS)

    def add_headline_to_image(self, image, headline, font_path='arial.ttf', font_size=40):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)
        text_width, text_height = draw.textsize(headline, font)

        width, height = image.size
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        draw.multiline_text((x, y), headline, font=font, fill=(255, 255, 255))
        return image
        
    def save_post(self, output_dir="generated_posts"):
        try:
            unique_id = int(time.time())
            output_path = Path(output_dir) / str(unique_id)
            output_path.mkdir(parents=True, exist_ok=True)

            sanitized_headline = self.sanitize_filename(self.news_headline)

            post_filename = output_path / f"{sanitized_headline[:10]}_post.txt"
            with open(post_filename, "w", encoding="utf-8") as post_file:
                post_file.write(f"Headline: {self.news_headline}\n\n")
                post_file.write(f"Image Prompt: {self.image_prompt}\n\n")
                post_file.write(f"Image URL: {self.image_url}\n\n")
                post_file.write(f"Description: {self.post_description}\n\n")

            image_response = requests.get(self.image_url)
            image = Image.open(io.BytesIO(image_response.content))

            resized_image = self.resize_image(image, (1080, 1080))
            image_with_heading = self.add_headline_to_image(resized_image, self.news_headline)

            image_filename = output_path / f"{sanitized_headline[:10]}_image.jpg"
            with open(image_filename, "wb") as image_file:
                image_with_heading.save(image_file, "JPEG")

            print(f"Post and image saved to {output_path}")
        except Exception as e:
            print(f"Error saving post and image: {e}")

def generate_post():
    post = Post("", "", "", "")
    post.generate_headline()
    if post.generated_news_headline is None:
        print("Failed to generate headline. Exiting.")
        return
    post.news_headline = Post.extract_headline(post.generated_news_headline)

    post.generate_image_prompt()
    if post.generated_image_prompt is None:
        print("Failed to generate image prompt. Exiting.")
        return
    post.image_prompt = Post.extract_image_prompt(post.generated_image_prompt)

    post.generate_post_description()
    if post.generated_post_description is None:
        print("Failed to generate post description. Exiting.")
        return
    post.post_description = Post.extract_post_description(post.generated_post_description)

    post.generate_image()
    if post.image_url is None:
        print("Failed to generate image. Exiting.")
        return

    # Save the post and image using the existing save_post function and the instance variables from the Post class.
    post.save_post()
