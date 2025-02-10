import cv2
import numpy as np
from PIL import Image, ImageDraw


def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars if c)


def generate_gyinjo_code(data, size=10):
    binary_data = text_to_binary(data)
    grid_size = int(np.ceil(np.sqrt(len(binary_data))))
    img_size = grid_size * size
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)
    
    for i, bit in enumerate(binary_data):
        x = (i % grid_size) * size
        y = (i // grid_size) * size
        if bit == '1':
            draw.ellipse([x, y, x + size, y + size], fill="black")
    
    img.save("gyinjo_code.png")
    img.show()


def decode_gyinjo_code(image_path, size=10):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    grid_size = img.shape[0] // size
    binary_data = ""
    
    for y in range(grid_size):
        for x in range(grid_size):
            region = img[y * size:(y + 1) * size, x * size:(x + 1) * size]
            if np.mean(region) < 128:
                binary_data += '1'
            else:
                binary_data += '0'
    
    return binary_to_text(binary_data)


# TESTING
text_message = "Hello, GYINJO!"
generate_gyinjo_code(text_message)
print("Decoded Text:", decode_gyinjo_code("gyinjo_code.png"))
