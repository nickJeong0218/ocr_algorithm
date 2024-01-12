import subprocess

try:
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    import re   
except ImportError:
    subprocess.run(['pip', 'install', 'fuzzywuzzy'])
    subprocess.run(['pip', 'install', 'python-Levenshtein'])
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    import re

'''This class is used to compare the text from the image to the data from Firestore.
It uses the fuzzywuzzy library to calculate the similarity between the two strings.
The score is calculated using the token_set_ratio, partial_ratio, and token_sort_ratio
algorithms. The highest score is returned along with the matched data.'''
class ScoreMatrix:
    def __init__(self, data_collection):
        self.data_collection = data_collection  # A list of dictionaries

    '''This method takes in a string and compares it to the data from Firestore.
    It returns the highest score and the matched data.
    The strings are first converted to uppercase and then split into a list of words.
    If the word is less than 2 characters, it is removed from the list.
    The score is calculated using the token_set_ratio, partial_ratio, and token_sort_ratio
    algorithms. The highest score is returned along with the matched data.'''
    def score(self, input_string):
        highest_score = -1
        matched_data = None

        # Remove all non-alphanumeric characters from the input string
        input_string = re.findall(r'[a-zA-Z0-9]+', input_string.upper())
        input_string = [word for word in input_string if len(word) > 2]

        for data in self.data_collection:
            # Convert float values to strings
            data_temp = {k: str(v) if isinstance(v, float) else v for k, v in data.items()}

            # Join the list into a single string for comparison
            data_string = ' '.join(str(v) for v in data_temp.values() if v is not None).upper()
            data_list = re.findall(r'[a-zA-Z0-9]+', data_string)
            
            # Calculate scores using different algorithms
            score_set = fuzz.token_set_ratio(input_string, data_list)
            score_partial = fuzz.partial_ratio(input_string, data_list)
            score_sort = fuzz.token_sort_ratio(input_string, data_list)

            # Get the highest score
            score = max(score_set, score_partial, score_sort)

            # If the score is higher than the current highest score, update the highest score
            if score > highest_score:
                highest_score = score
                matched_data = data

        return highest_score, matched_data