from connect_db.firebase_manager import FirebaseManager
from text_extraction.image_enhancer import ImageProcessor
from text_extraction.ocr_process import OCRProcessor
from score_matrix.scoring import ScoreMatrix

'''This is the main driver for the OCR project.'''
def main():
    CONFIDENTIAL_KEY_PATH = '/Users/nickjeong/Documents/OCR/ocr-project-2f105-firebase-adminsdk-6079j-3832fb8510.json'
    STORAGE_URL = 'ocr-project-2f105.appspot.com'

    # Initialize Firebase
    fb_app = FirebaseManager(CONFIDENTIAL_KEY_PATH, STORAGE_URL)
    print('Connected to Firebase.')

    # Load data from Firestore
    data_collection = fb_app.get_all_documents('test')

    # Load an input image and preprocess it.
    image_path = '/Users/nickjeong/Documents/OCR/test_data/20231113_112622.jpg'
    image = ImageProcessor(image_path)
    print('Loaded image from', image_path)

    image.preprocess_image()
    image.detect_text_regions()
    print('Preprocessed image.')

    preprocessed_image = image.get_image()
    print('Preprocessed image is ready.')

    # Apply OCR to the preprocessed image.
    ocr = OCRProcessor(preprocessed_image)
    ocr.apply_ocr()
    text_from_image = ocr.get_text()
    print('Applied OCR to the preprocessed image.')

    # Compare the text from the image to the data from Firestore.
    score_matrix = ScoreMatrix(data_collection)
    score, matched_data = score_matrix.score(text_from_image)

    # Print the matched data.
    print('--------------------------------------------------')
    print('With a score of', score, 'the matched data is:\n')
    for(key, value) in matched_data.items():
        print(key, ':', value)
    print('--------------------------------------------------')

    # Disconnect from Firebase
    fb_app.disconnect_firebase()
    print('Disconnected from Firebase.')

if __name__ == '__main__':
    main()