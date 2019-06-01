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
       c.Output = "scraped"
       twint.run.Search(c)

#list = ["Nidalgazaui", "#sahawat", "taghut", "kufr", "dawlah"]
# list = ["alawite", "manhaj", "rafidah", "kuffar"]
list = ["ابو نعيمان"]

scrape(list[0])
