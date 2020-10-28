# NBA-Scraper
NBA Scraper - Scrapes current NBA player data from basketball-reference.com (WORK IN PROGRESS)

========================
scraper.py
========================
This scraper creates the necessary files in the local C:\NBA Scraper folder (will create the folder if it does not exist)
and then scrapes basketball-reference.com for links on all current NBA players. 

========================
csv_script.py
========================
This script will take all the links obtained from scraper and create a players folder within the scraper folder and then
add all the current NBA players data to individual Folders and.csv files based upon their season played. 


========================
To Do:
========================
-Clean up the code and logic
-Finish csv_script.py
-Allow for a more dynamic approach (ex. allow users to create the necessary folders in the location of their choice)
-Incorporate the .csv data into a MySQL database
-Incorporate Django and upload the data onto an interactive personal site
-Add a virtual interactive betting system based upon the data and the next current game to be played on AWS
