from firebase_manager import FirebaseManager

CONFIDENTIAL_KEY_PATH = '/Users/nickjeong/Documents/OCR/ocr-project-2f105-firebase-adminsdk-6079j-3832fb8510.json'
STORAGE_URL = 'ocr-project-2f105.appspot.com'

def main():
    '''Firebase Storage'''
    fb_app = FirebaseManager(CONFIDENTIAL_KEY_PATH, STORAGE_URL)
    print('Connected to Firebase Storage')

    # # Insert data into Firestore
    # fb_app.add_document('test', 'test_doc1', {'name': 'Nick', 'age': 24})

    # # Insert image into Storage
    # storage_file_path = 'images/test_image.jpg'
    # fb_app.upload_file('/Users/nickjeong/Documents/OCR/connect_db/test_image.jpg', storage_file_path)

    # # Upload image from URL into Storage
    # fb_app.upload_image_from_url('https://drinkzyn.com/cdn/shop/files/bicepss_1024x1024.jpg?v=1669974342', 'images/google_logo.png')

    # # Get data from Storage
    # fb_app.download_file('images/test_image.jpg', '/Users/nickjeong/Documents/OCR/connect_db/test_image_downloaded.jpg')

    # # Get a file from Storage that is uploaded from local
    # fb_app.download_file('images/test_url.png', '/Users/nickjeong/Documents/OCR/connect_db/test_image_downloaded_url.jpg')

    # # Get a file from Storage that is uploaded through the URL of the image
    # image_url = f"{fb_app.bucket_url}/{storage_file_path}"

    # # Get a file from Storage that indicates the image was uploaded in Firestore
    # fb_app.download_file('images/test_image.jpg', '/Users/nickjeong/Documents/OCR/connect_db/test_image_firestore.jpg')

    # data = {'brand': 'test_brand', 
    #         'product name': 'test1', 
    #         'type': 'test_type',
    #         'description': 'test_description',
    #         'price': 1.99, 
    #         'quantity': 1, 
    #         'size': '1 oz',
    #         'SKU': 'test1', 
    #         'image': image_url}

    # # Insert data into Firestore
    # fb_app.add_document('test', 'test_doc1', data)

    # for doc in fb_app.get_all_documents('test'):
    #     print(doc)

    print(fb_app.get_document('test', 'image1'))

    # Disconnect from Firestore and Storage
    fb_app.disconnect_firebase()
    
    
main()