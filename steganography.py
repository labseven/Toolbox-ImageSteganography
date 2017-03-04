"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for x in range(x_size):
        for y in range(y_size):
            if lsb_of_red_pixel(encoded_image, x, y):
                pixels[x, y] = (255,255,255)
            else:
                pixels[x, y] = (0, 0, 0)

            #pixels[x, y] = [(0,0,0) if lsb_of_pixel(red_channel, x, y) else (1,1,1)]

    decoded_image.save("images/decoded_image.png")
    decoded_image.show()

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/samoyed.jpg", output_image="images/samoyed.secret.png"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """

    image = Image.open(template_image)
    pixels = image.load()

    x_size = image.size[0]
    y_size = image.size[1]

    for x in range(x_size):
        for y in range(y_size):
            if lsb_of_red_pixel(image, x, y):
                pixels[x,y] = (image.getpixel((x, y))[0] - 1, image.getpixel((x, y))[1], image.getpixel((x, y))[2])

    text_image = Image.new("RGB", image.size)

    usr_font = ImageFont.truetype("ComicNeue.otf", 25)
    d_usr = ImageDraw.Draw(text_image)
    d_usr = d_usr.text((10,10), text_to_encode, (255,255,255), font=usr_font)

    for x in range(x_size):
        for y in range(y_size):
            if lsb_of_red_pixel(text_image, x, y):
                pixels[x,y] = (image.getpixel((x, y))[0] + 1, image.getpixel((x, y))[1], image.getpixel((x, y))[2])

    image.save(output_image)



def lsb_of_red_pixel(image, x, y):
    return image.getpixel((x, y))[0] % 2

if __name__ == '__main__':
    # print("Decoding the image...")
    # decode_image()

    print("Encoding the image...")
    encode_image("Hi meme")

    print("Decoding Encoded image...")
    decode_image("images/samoyed.secret.png")
