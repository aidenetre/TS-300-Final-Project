import main
from PIL import Image

def test_main():

    headline = "Carney: Fed Will Start Taper in Late 2023"

    image = Image.open("C:/Users/AidenMacdonald/OneDrive - Aiden Macdonald/Documents/GitHub/TS-300-Final-Project/generated_posts/1680590415/   Carney__image.jpg")

    image_with_headline = main.add_headline_to_image(image, headline)

    image_with_headline.save("generated_posts/1680590415/Carney__image_with_headline.jpg")
    return 0

test_main()