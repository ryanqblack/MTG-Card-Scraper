# MTG-Card-Scraper
This Python script goes to the MTG website and scrapes every single card off their website.

It will return the following information:
 - Card Name
 - Converted Mana Cost
 - Mana Cost
 - Type
 - Card Text
 - Expansion
 - Rarity
 - Card Number
 - P/T
 - Artist
 - Community Rating out of 5

# Setup
You will need to download "geckodriver" as this uses Firefox to get HTML source code. You will also need the latest version of Python.

Python will require libraries to run properly:
 - lxml
 - beautifulsoup4
 - selenium

Once these dependencies are installed, you may run the script using "py Magic.py" in a terminal.

# What's next?
 - Make improvements in efficiency (writing to the file as it reads data instead of after all the data has been read in)
