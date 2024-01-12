from image_enhancer import ImageProcessor
from ocr_process import OCRProcessor

def main():
    # Step 1: Load the image
    image_path = '/Users/nickjeong/Documents/OCR/test_data/20231113_112622.jpg'
    image = ImageProcessor(image_path)

    image.preprocess_image()
    image.detect_text_regions()

    result = image.get_image()

    result.show()

    ocr = OCRProcessor(result)
    ocr.apply_ocr()
    print(ocr.get_text())

main()