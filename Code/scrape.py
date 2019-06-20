"""
Kickstarts preprocessing pipeline -> start()

Scrapes Twitter using the twint tool.

"""
import twint
import os
from time import sleep

import translate
import cleaning
import dataprocessing
import bert_eval


# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape(keyword):
       c = twint.Config()
       # c.Username = "twitter" # If you wanted to do username search.
       c.Search = keyword
       c.Store_csv = True
       # CSV Fieldnames
       c.Custom["tweet"] = ["hashtags", "date", "time", "id", "name", "username", "tweet"]
                            # After preprocessing, data has add. columns: translated, cleaned
       # Name of the directory
       c.Output = "input_data" # Output directory name. tweets will be in this folder as 'tweets.csv'
       c.Limit = 20 # Limited to scraping 2000 tweets for now, 800 for testing
       twint.run.Search(c)

# use scrape(input_word) to scrape twitter for the data.
def start(keyword):
       DATA_PATH = './input_data/tweets.csv'
       FOLDER = './input_data'
       # Remove any old tweets.csv
       try:
              os.remove('./input_data/tweets.csv')
              print("Removed tweets.csv")
       except OSError as e:
              logger.error("tweets.csv has not been created yet. " + str(e))

       # Scrape twitter for tweets and save it in input_data/tweets.csv
       print("Scraping...")
       scrape(keyword) # fakeuseragent error always happens here; it does not affect function.
       sleep(2) # Give time for the file to be created

       # Assert there is a new tweets.csv
       assert os.path.exists(DATA_PATH), "tweets.csv does not exist."
       print("Scraping finished. Translation being performed...")

       # Translate tweet column.
       translate.translate(DATA_PATH)
       print("Translation complete. Cleaning in progres...")
       # Clean the data
       cleaning.clean(DATA_PATH)
       print("Cleaning complete. Converting to tsv...")
       # Change it into correctly formatted .tsv
       # In case there is already an old dev.tsv
       try:
              os.remove('./input_data/dev.tsv')
              print("Removed dev.tsv")
       except OSError as e:
              pass

       dataprocessing.change_to_tsv(DATA_PATH, FOLDER)
       print("Preprocessing complete. Processing...")
       # Put it into BERT. >> Remember to make BERT save the predictions somewhere
       bert_eval.predict(FOLDER)
       print("View results at ./outputs/results/results.csv")


