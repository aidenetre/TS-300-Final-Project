import os
import openai
import requests
import re
from datetime import date
from pathlib import Path

# Set up OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_headline(initial_prompt):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = initial_prompt,
        max_tokens = 100,
        temperature = 0.7,
        top_p = 1,
    )

    return response["choices"][0]["text"].strip()

def generate_image_prompt(fake_news_headline):

    image_prompt = f"Write a sentence describing the image in an instagram post relating to the financial news headline: {fake_news_headline} using the following template: PROMPT: <A [format] of [scene] in the style of [style], [perspective].> You need to replace the parameters in the brackets. Use the following lists to choose from for each one: format: ... style: ... perspective: ... The scene parameter needs to specify an object or subject performing an action. Describe the scenery. Describe the mood and the lighting."

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": image_prompt}],
        max_tokens = 2000,
        temperature = 0.7,
        top_p = 1,
    )

    image_prompt_response = response["choices"][0]["message"]["content"]

    return image_prompt_response

def generate_post(fake_news_headline):

    description_prompt = f"Create an instagram post for the following financial news headline: {fake_news_headline} using the following template: DESCRIPTION: <description including hashtags and emojis>"

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": description_prompt}],
        max_tokens = 2000,
        temperature = 0.7,
        top_p = 1,
    )

    post_response = response["choices"][0]["message"]["content"]

    return post_response

def extraction(instagram_post):
    # Find the index of "PROMPT: "
    prompt_index = instagram_post.find("PROMPT: ") + len("PROMPT: ")

    # Find the index of the end of the prompt (which is marked by a newline)
    prompt_end_index = instagram_post.find("DESCRIPTION: ", prompt_index)

    # Extract the prompt
    image_prompt = instagram_post[prompt_index:prompt_end_index].strip()

    # Find the index of "DESCRIPTION: "
    description_index = instagram_post.find("DESCRIPTION: ") + len("DESCRIPTION: ")

    # Extract the description
    post_description = instagram_post[description_index:].strip()

    print("image_prompt: " +image_prompt)
    print("description: " +post_description)

    return image_prompt, post_description

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        num_images=1,
    )

    print(prompt)

    return response["data"][0]["url"]

def sanitize_filename(filename):
    # Replace any characters that are not letters, numbers, or spaces with underscores
    return re.sub(r'[^\w\s]+', '_', filename)

def save_post(fake_news_headline, image_prompt, image_url, post_description, output_dir="generated_posts"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Sanitize headline for use in file name
    sanitized_headline = sanitize_filename(fake_news_headline)

    # Save post and description to text file
    post_filename = output_path / f"{sanitized_headline[:10]}_post.txt"
    with open(post_filename, "w", encoding="utf-8") as post_file:
        post_file.write(f"Headline: {fake_news_headline}\n\n")
        post_file.write(f"Image Prompt: {image_prompt}\n\n")
        post_file.write(f"Image URL: {image_url}\n\n")
        post_file.write(f"Description: {post_description}\n\n")

    # Save image to file
    image_response = requests.get(image_url)
    image_filename = output_path / f"{sanitized_headline[:10]}_image.jpg"
    with open(image_filename, "wb") as image_file:
        image_file.write(image_response.content)

    print(f"Post and image saved to {output_path}")

def main():
    today = date.today()
    fake_news_prompt = f"Generate a current financial news headline for the current date {today}:"
    fake_news_headline = generate_headline(fake_news_prompt)
    generated_image_prompt = generate_image_prompt(fake_news_headline)
    generated_description = generate_post(fake_news_headline)
    post = str(generated_image_prompt) + "   " + str(generated_description)
    image_prompt, post_description = extraction(post)
    image_url = generate_image(image_prompt)

    save_post(fake_news_headline, image_prompt, image_url, post_description)

if __name__ == "__main__":
    main()
