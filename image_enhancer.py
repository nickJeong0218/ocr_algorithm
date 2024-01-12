import subprocess

try:
    import cv2
    import numpy as np
    from PIL import Image
except ImportError:
    subprocess.run(['pip', 'install', 'opencv-python'])
    subprocess.run(['pip', 'install', 'Pillow'])

    import cv2
    import numpy as np
    from PIL import Image

'''This class is used to preprocess the image before applying OCR.
It uses OpenCV to apply Gaussian blur, Canny edge detection, and thresholding.
It also uses OpenCV to find contours in the image and filter out small contours.
Finally, it uses OpenCV to draw the contours on the original image.'''
class ImageProcessor:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    '''This method resizes the image to a width/height of 3000 pixels while maintaining the aspect ratio.
    It then converts the image to grayscale and applies Gaussian blur to reduce noise.
    It then applies Canny edge detection and thresholding to separate text from the background.
    Finally, it applies contrast enhancement to make the text more visible.'''
    def preprocess_image(self):
        # Get the aspect ratio of the image
        height, width = self.image.shape[:2]

        if width < height:
            new_width = 3000
            aspect_ratio = height / width

            # Calculate the new height while maintaining the aspect ratio
            new_height = int(new_width * aspect_ratio)
        else:
            new_height = 3000
            aspect_ratio = width / height

            # Calculate the new width while maintaining the aspect ratio
            new_width = int(new_height * aspect_ratio)

        # Resize the image
        self.image = cv2.resize(self.image, (new_width, new_height))

        # Convert the image to grayscale
        grayscale = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blur = cv2.GaussianBlur(grayscale, (5, 5), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(blur, 5, 115)

        # Apply thresholding to separate text from the background
        _, threshold = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        self.image = threshold

        # Apply contrast enhancement
        self.image = cv2.convertScaleAbs(self.image, alpha=1.5, beta=0)

    '''This method applies skew correction to the image.
    It then finds contours in the image and filters out small contours.
    Finally, it draws the contours on the original image.'''
    def detect_text_regions(self):
        # Apply skew correction
        coords = np.column_stack(np.where(self.image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.image = cv2.warpAffine(self.image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out small contours based on area
        min_area = 50
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

        # Draw the contours on the original image
        self.image = cv2.drawContours(self.image, contours, -1, (0, 255, 0), 3)

    '''This method converts the image to a PIL Image object and returns it.'''
    def get_image(self):
        return Image.fromarray(self.image)