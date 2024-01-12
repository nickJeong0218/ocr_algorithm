import subprocess

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, storage
    import google.cloud.exceptions
    import requests
    import tempfile
except ImportError:
    subprocess.run(['pip', 'install', 'firebase-admin'])
    subprocess.run(['pip', 'install', 'google-cloud-storage'])
    subprocess.run(['pip', 'install', 'requests'])

    import firebase_admin
    from firebase_admin import credentials, firestore, storage
    import google.cloud.exceptions
    import requests
    import tempfile

class FirebaseManager:
    '''This contains methods to connect to Firestore and Storage, and to add, update, and delete data in Firestore,
    and to upload, download, and delete files in Storage.'''
    def __init__(self, cred_path, bucket_url):
        self.cred_path = cred_path
        self.bucket_url = bucket_url
        self.connect_firebase()

    '''This method will connect to Firestore and Storage.
    It will also initialize the Firestore and Storage instances.'''
    def connect_firebase(self):
        cred = credentials.Certificate(self.cred_path)

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {'storageBucket': self.bucket_url})

        # Get a reference to Firestore and Storage
        self.db = firestore.client()
        self.bucket = storage.bucket()

    '''This method will add a document to the specified collection in Firestore.
    collection: name of the collection
    document_id: name of the document
    data: dictionary of data to add to the document'''
    def add_document(self, collection, document_id, data):
        # Get a reference to the document
        doc_ref = self.db.collection(collection).document(document_id)

        # Set the data
        doc_ref.set(data)

    '''This method will get a document in the specified collection in Firestore.
    collection: name of the collection
    document_id: name of the document'''
    def get_document(self, collection, document_id):
        # Get a reference to the document
        doc_ref = self.db.collection(collection).document(document_id)
        try:
            # Get the document
            doc = doc_ref.get()

            # Return the document data
            return doc.to_dict()
        except google.cloud.exceptions.NotFound:
            # If the document does not exist, return None
            return None
    
    '''This method will get all documents in the specified collection in Firestore.
    collection: name of the collection'''
    def get_all_documents(self, collection):
        # Get a reference to the collection
        col_ref = self.db.collection(collection)

        # Get all documents in the collection
        docs = col_ref.stream()

        docs_list = [doc.to_dict() for doc in docs]

        # Return the documents
        return docs_list

    '''This method will delete a document in the specified collection in Firestore.
    collection: name of the collection
    document_id: name of the document'''
    def delete_document(self, collection, document_id):
        # Get a reference to the document
        doc_ref = self.db.collection(collection).document(document_id)

        # Delete the document
        doc_ref.delete()

    '''This method will add a file to the specified folder in Storage.
    local_file_path: path to the local file
    storage_file_path: path to the file in Storage'''
    def upload_file(self, local_file_path, storage_file_path):
        # Get an instance of a Storage Blob
        blob = self.bucket.blob(storage_file_path)

        # Open a local file to read
        with open(local_file_path, 'rb') as file:
            # Upload the file to Firebase Storage
            blob.upload_from_file(file)

    '''This method will add an image from a URL to the specified folder in Storage.
    url: URL of the image
    storage_file_path: path to the file in Storage'''
    def upload_image_from_url(self, url, storage_file_path):
        # Get a response from the URL
        response = requests.get(url)

        # Download the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            # Write the content of the response to the temporary file
            temp_file.write(response.content)

            # Flush the data to the temporary file
            temp_file.flush()

            # Get an instance of a Storage Blob
            blob = self.bucket.blob(storage_file_path)

            # Open the temporary file to read
            with open(temp_file.name, 'rb') as file:
                # Upload the image to Firebase Storage
                blob.upload_from_file(file)

    '''This method will download a file from Storage.
    storage_file_path: path to the file in Storage
    local_file_path: path to the local file'''
    def download_file(self, storage_file_path, local_file_path):
        # Get an instance of a Storage Blob
        blob = self.bucket.blob(storage_file_path)

        # Download the file to a local file
        with open(local_file_path, 'wb') as file:
            # Download the file from Firebase Storage
            blob.download_to_file(file)

    '''This method will delete a file from Storage.
    storage_file_path: path to the file in Storage'''
    def delete_file(self, storage_file_path):
        # Get an instance of a Storage Blob
        blob = self.bucket.blob(storage_file_path)

        # Delete the file from Firebase Storage
        blob.delete()
    
    '''This method will disconnect from Firestore and Storage.
    It will also delete the app.
    This method should be called when you are done using Firestore and Storage.'''
    def disconnect_firebase(self):
        # Delete the app
        firebase_admin.delete_app(firebase_admin.get_app())