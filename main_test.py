import unittest
from PIL import Image
from main import binary_to_image

class TestImageBinaryConverter(unittest.TestCase):

    def test_binary_to_image(self):
        # Test with odd-length binary string
        binary_string = "11010101010101101"
        binary_to_image(binary_string)
        # Load the resulting image
        img = Image.open("image17.png")
        # Check the image size
        self.assertEqual(img.size, (1280, 720))
        # Clean up
        img.close()



