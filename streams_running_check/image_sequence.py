import os
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer, util

# Init constants
TRESHHOLD = 0.92
PIXEL_DIFFERENCE_THRESHOLD = 8
SCREENSHOTS_FOLDER = 'screenshots/'
# Load the pre-trained model
model = SentenceTransformer('clip-ViT-B-32')


def screenshot_similarity() -> bool:
    """
    Compares screenshots in the screenshots folder for pixel and semantic similarity.

    Returns:
        bool: True if all screenshots are similar, False otherwise.
    """
    result = []
    screenshot_files = os.listdir(SCREENSHOTS_FOLDER)
    # first screenshot to compare with others
    compar_screenshot = screenshot_files[0]
    for screenshot in screenshot_files[1:]:
        pixel_diff_result = check_pixel_difference(compar_screenshot, screenshot)
        semantic_diff_result = semantic_difference(compar_screenshot, screenshot)
        # Check if both pixel and semantic differences are within the threshold
        if pixel_diff_result and semantic_diff_result:
            result.append(1)
        else:
            result.append(0)
    # Calculate the score based on the results
    score = sum(result) / len(result)
    return score == 1.0


def check_pixel_difference(screenshot_1:str, screenshot_2:str) -> bool:
    """
    Compares two screenshots pixel by pixel and checks if the difference is less than 5%.

    Args:
        screenshot_1 (str): The filename of the first screenshot.
        screenshot_2 (str): The filename of the second screenshot.
    
    Returns:
        bool: True if the difference is less than 5%, False otherwise.
    """
    # Image 1 and Image 2
    img_1 = Image.open(f'{SCREENSHOTS_FOLDER}{screenshot_1}')
    img_2 = Image.open(f'{SCREENSHOTS_FOLDER}{screenshot_2}')
    # Array 1 and Array 2
    arr_1 = np.array(img_1)
    arr_2 = np.array(img_2)
    # Vectors 1 and 2
    vec_1 = arr_1.flatten().tolist()
    vec_2 = arr_2.flatten().tolist()
    # Check if difference pixel in the sequence is less than 5%
    difference = list()
    # Iterate through the vectors and compare each pixel value
    for index in range(len(vec_1)):
        # Check if the pixel values are different
        if vec_1[index] != vec_2[index]:
            difference.append(1) # Append a marker for difference
    print(f"Difference between vectors: {len(difference)}")
    diff_percentage = len(difference) / len(vec_1) * 100
    # Return True if less than 5% difference 
    return diff_percentage <= 5

def semantic_difference(screenshot_1:str, screenshot_2:str) -> bool:
    """
    Compares two screenshots semantically using a pre-trained model.

    Args:
        screenshot_1 (str): The filename of the first screenshot.
        screenshot_2 (str): The filename of the second screenshot.
    
    Returns:
        bool: True if the semantic similarity is above a certain threshold, False otherwise.
    """
    # Load images and convert to base64
    img_1 = Image.open(f'{SCREENSHOTS_FOLDER}{screenshot_1}')
    img_2 = Image.open(f'{SCREENSHOTS_FOLDER}{screenshot_2}')
    
    # Encode images
    img_1_embedding = model.encode(img_1, convert_to_tensor=True)
    img_2_embedding = model.encode(img_2, convert_to_tensor=True)
    
    # Calculate cosine similarity
    similarity = util.pytorch_cos_sim(img_1_embedding, img_2_embedding)
    
    # Define a threshold for semantic similarity
    return similarity.item() >= TRESHHOLD