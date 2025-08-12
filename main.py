import time
from bot import run_driver
import pandas as pd
from streams_running_check.image_sequence import screenshot_similarity
from slack_bot import slack_send_message

df = pd.read_csv("production_streams.csv")
data = [{"url": row["url"], "label": row["label"]} for index, row in df.iterrows()]

if __name__ == "__main__":
    while True:
        print("Checking streams...")
        for row in data:
            # Init variables
            url, label = row["url"], row["label"]
            content = f"""
            LABEL: {label}
            STREAM: {url} 
            It’s not working, no changes are happening in the video or does not work.
            """
            # Run the driver and take screenshots
            if run_driver(url):
                print("Driver ran successfully and screenshots were taken.")
            else:
                print("There was an error running the driver or taking screenshots.")
                slack_send_message(content)
            print("Checking screenshot similarity...")
            if screenshot_similarity():
                slack_send_message(content)
                print(content)
                print("-"*30)
            else:
                print("All streams are running fine, no changes detected.")
        slack_send_message("All streams have been checked.")