"""
Scrapes Twitter using the twint tool.

"""
import twint

# Configure
def scrape(keywords):
       c = twint.Config()
       # c.Username = "twitter"
       c.Search = keywords
       c.Store_csv = True
       # CSV Fieldnames
       c.Custom["tweet"] = ["hashtags", "date", "time", "id", "name", "username", "tweet"]
       # Name of the directory
       c.Output = "patch2" # Output directory name. tweets will be in this folder as 'tweets.csv'
       twint.run.Search(c)



for word in list:
       try:
              scrape(word)
       except Exception as e:
              print("error ", e)
