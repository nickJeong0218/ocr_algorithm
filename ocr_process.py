import subprocess

try:
    import pytesseract
    from PIL import Image
    from textblob import TextBlob
    import re
except ImportError:
    subprocess.run(['pip', 'install', 'pytesseract'])
    subprocess.run(['pip', 'install', 'Pillow'])
    subprocess.run(['pip', 'install', 'textblob'])
    # Import necessary libraries
    import pytesseract
    from PIL import Image
    from textblob import TextBlob
    import re

'''This class is used to apply OCR to the image.
It uses pytesseract to convert the image to text.
It also uses TextBlob to correct spelling and replace continuous O's with 0's for SKU codes.'''
class OCRProcessor:
    def __init__(self, image):
        self.image = image

    '''This method applies OCR to the image and returns the text.'''
    def apply_ocr(self):
        custom_oem_psm_config = r'--oem 3 --psm 3'

        # Apply OCR to the image
        self.text = pytesseract.image_to_string(self.image, config=custom_oem_psm_config)

        # Correct spelling and replace continuous O's with 0's
        self.text = self.correct_text(self.text)

    '''This method uses TextBlob to correct spelling and replace continuous O's with 0's for SKU codes.'''
    def correct_text(self, text):
        # Use TextBlob to correct spelling
        corrected_text = TextBlob(text).correct()

        # Replace continuous O's with 0's
        corrected_text = re.sub(r'([Oo]{3,})', '000', str(corrected_text))

        return str(corrected_text)

    '''This method returns the text from the image.'''    
    def get_text(self):
        return self.text