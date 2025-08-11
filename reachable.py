from typing import Dict, Union
import requests
from bs4 import BeautifulSoup

TRESSHOLD = 400 # Website status code threshold success 

def check_website(url:str) -> Dict[str, Union[bool, int, str]]:
    """
    Checks if a website is reachable and returns its status.

    Args:
        url (str): The URL of the website to check.

    Returns:
        Dict[str, Union[bool, int, str]]: A dictionary containing the 
        status of the website and also several other informations.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=5)
        # Check if the status code is less than the threshold
        status = response.status_code < TRESSHOLD
        soup = BeautifulSoup(response.content, 'lxml')
        if not soup.select_one("video"):
            raise requests.RequestException("No video found on the page.")
        print(response.status_code)
        return {"status_code": response.status_code,
                "reachable": status,
                "url": url,
                "error": None,
                "message": "Website is reachable" if status else "Website is not reachable"}
    except requests.RequestException as e:
        return {"status_code": None,
                "reachable": False,
                "url": url,
                "error": str(e),
                "message": "Website is not reachable due to an exception"}


if __name__ == "__main__":
    url = "https://app.womansworldcup.spovizz.com/frontend/timeline/0ba816e5-d31a-4fbb-87eb-788336d01b84?format=1920x1080&lng=de&stream=audio"
    result = check_website(url)
    print(f"Checking website {result}...")