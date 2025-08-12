from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Set Chrome options
opts = Options()
# Init constants
SCREENSHOTS_DIR = 'screenshots/'  # Folder for screenshots
BEGINNING_DELAY = 10 # Delay before starting the screenshot process
SCREENSHOT_AMOUNTS = 5  # Amount of screenshots to take
TIME_DELAY = 5  # Delay between screenshots in seconds

# Init the driver
opts = webdriver.ChromeOptions()  # Headless-Modus for the Browser
# opts.add_argument('--headless')
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument("--window-size=1920,1080")
opts.add_argument("--log-level=3")
opts.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=opts)
driver.maximize_window()

def run_driver(url:str) -> bool:
    """
    Runs the Selenium WebDriver to take screenshots of a webpage.

    Args:
        url (str): The URL of the webpage to take screenshots of.
    
    Returns:
        bool: True if the screenshots were taken successfully, False otherwise.
        And also if the browser is running or successfully closed.
    """
    # Maximize the browser window
    try:
        print(f"Opening URL: {url}")
        driver.get(url)
        print("Opened URL successfully.")
        sleep(BEGINNING_DELAY)  # Wait for the page to load
        # Check if the page has loaded correctly
        for index in range(SCREENSHOT_AMOUNTS):
            filename = f'{SCREENSHOTS_DIR}screenshot_{index}.png'
            driver.save_screenshot(filename)
            print(f"Screenshot saved: {filename}")
            sleep(TIME_DELAY)
        print("All screenshots taken successfully.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        quit_driver(driver)
        return False


def quit_driver(driver:webdriver.Chrome) -> None:
    """
    Closes the Selenium WebDriver.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance to close.
    
    Returns:
        None
    """
    driver.close()  # Close the browser
    driver.quit()  # Quit the driver
