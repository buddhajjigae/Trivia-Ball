import requests
import csv
import sys
import re
import os
from bs4 import BeautifulSoup
from string import ascii_lowercase
from time import sleep
from os import path

#########################################################
'''                      METHODS                      ''' 
#########################################################

'''Generates the name of the file to be created'''
def file_name(URL, playername):
    l = URL.split('/')[-3:]
    filename = playername + '-' + '-'.join(l) + ".csv"
    
    if filename[-5:] == "-.csv":
        filename = filename.replace("-.csv", ".csv")
        
    return filename

'''Finds the URL of each Game Log for the Player'''
def get_game_logs(url):
    game_url = 'https://www.basketball-reference.com' + url
    result = []
    
    page = requests.get(game_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    logs = soup.find("li", { "class" : "full hasmore"})

    for i in logs:
        td = logs.find_all('a')
        for j in td:
            glog = j.get('href')
            result.append('https://www.basketball-reference.com' + glog)
    result = list(dict.fromkeys(result))
    
    return result

'''Gets the headers of the data table'''
def get_headers(table):
    thead = table.find('thead')
    th_head = thead.find_all('th')
    fields = []

    for thh in th_head:
        fields.append(thh.get('data-stat'))
    
    return fields

'''Gets the players that are currently playing'''
def get_players(url):
    player_url = url
    page = requests.get(player_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table", { "id" : "players" })
    names = player_names(table)
    
    return names

'''Gets the player name for the file'''
def get_player_name(name):
    for n in name:
        n1 = name.string
        n2 = re.split(' \d+', n1)
        n2 = n2[0]

    j = n2.split()
    
    if len(j) == 2:
        player_name = j[1] + "_" + j[0]
    else:
        player_name = j[1] + "_" + j[0] + "_" + j[2]
   
    if os.path.isdir(player_name):
        return player_name
    else:     
        os.mkdir(player_name)

    return player_name

'''Generates a list of all the data values'''
def make_table_list(table):
    result = []
    table_rows = table.find_all('tr')
    
    for tr in table_rows:
        td = tr.find_all('th') + tr.find_all('td')
        row = [i.text for i in td]
        result.append(row)
    
    for i, e in enumerate(result):
        if e[0] == "Rk":
            result.pop(i)
    
    return result

'''Gets the URL's for each active player'''
def player_names(table):
    result = []
    table_rows = table.find_all('strong')
    
    for tr in table_rows:
        td = tr.find_all('a')
        #row = [i.get('href') for i in td]
        for i in td:
            row = i.get('href')
            result.append(row)

    return result    

'''Writes to completed file to ignore'''
def write_completed(url):
    with open(r'C:\NBA Scraper\Completed.txt', 'a') as txtfile:
        txtfile.write(url + "\n")

'''Writes the headers into the CSV file'''
def write_headers(headers, filename):
    with open(filename, 'w') as csvfile:  
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(headers)  
    
'''Writes the data rows into the CSV file'''    
def write_rows(filename, data):
    with open(filename, 'a') as csvfile:  
        writer = csv.writer(csvfile, delimiter = ',')
        i = 0
        for e in data:
            writer.writerow(data[0+i]) 
            i += 1  
       
'''Writes the URL's that will be scraped into a txt file'''
def write_urls_text(names, alphabet):
    with open(r"C:\NBA Scraper\Game_Logs.txt", "a") as textfile:
        for i in names:
            logs = get_game_logs(i)
            for j in logs: 
                textfile.write(j + "\n")
            
    print("Finished Writing To File:   Game_Logs.txt || Letter: " + alphabet)      

#########################################################
'''                    MAIN CODE                      ''' 
#########################################################

print("***STARTING NBA SCRAPER***")

'''Generate Necessary Directories and Files'''
if os.path.isdir(r"C:\NBA Scraper") == True:
    print(r"C:\NBA Scraper\   Directory Exists, Will Not Create Directory")
else:
    os.chdir(r"C:\\")
    os.mkdir("NBA Scraper")
    print(r"C:\NBA Scraper\   Created")


if os.path.isdir(r"C:\NBA Scraper\players") == True:
    print(r"C:\NBA Scraper\players   Directory Exists, Will Not Create Directory")
else:
    os.chdir(r"C:\NBA Scraper\\")
    os.mkdir("players")
    print(r"C:\NBA Scraper\players   Created")
    
    
if os.path.isdir(r"C:\NBA Scraper\teams") == True:
    print(r"C:\NBA Scraper\teans   Directory Exists, Will Not Create Directory")
else:
    os.chdir(r"C:\NBA Scraper\\")
    os.mkdir("teams")  
    print(r"C:\NBA Scraper\teams   Created")


if path.exists(r"C:\NBA Scraper\Completed.txt") == False:
    os.chdir(r"C:\NBA Scraper\\")
    comp_file = open('Completed.txt','w')
    comp_file.close()
    print("Created Completed.txt")
else:
    print(r"C:\NBA Scraper\Completed.txt   File Exists, Will Not Create File")
    

if path.exists(r"C:\NBA Scraper\Game_Logs.txt") == False:
    os.chdir(r"C:\NBA Scraper\\")
    logs = open('Game_Logs.txt','w')
    logs.close()
    print("Created Game_Logs.txt")
else:
    os.remove(r'C:\NBA Scraper\Game_Logs.txt')
    os.chdir(r"C:\NBA Scraper\\")
    logs = open('Game_Logs.txt','w')
    logs.close()
    print("Created Game_Logs.txt")

'''ITERATE THROUGH SITE FOR TESTING'''
names = get_players('https://www.basketball-reference.com/players/' + 'a')
write_urls_text(names, 'a')

# '''Generate Game Logs''' Uncomment to iterate through entire player database
# for i in ascii_lowercase:
#     names = get_players('https://www.basketball-reference.com/players/' + i)
#     write_urls_text(names, i)

'''Read Game_Logs.txt and delete after reading'''
logs = open(r'C:\NBA Scraper\Game_Logs.txt','r').read().split('\n')
print(len(logs))
os.remove(r'C:\NBA Scraper\Game_Logs.txt')
print("***Game_Logs.txt DELETED***")

'''Read Completed.txt'''
#comp_file = open(r'C:\NBA Scraper\Completed.txt','r')
#comp_logs = comp_file.readlines()
#comp_file.close()
comp_logs = open(r'C:\NBA Scraper\Completed.txt','r').read().split('\n')

'''Scraper Counters'''
comp_counter = 0
ncomp_counter = 0

'''Player Scraper'''
for log in logs:
    if log not in comp_logs:
        comp_counter += 1
        URL = log.replace("\n", "")
        sleep(3)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        os.chdir(r"C:\NBA Scraper\players")
        player_name = get_player_name(soup.find('h1', itemprop="name"))
        filename = file_name(URL, player_name)
        table = soup.find(class_="table_outer_container")
        headers = get_headers(table)
        player_dir = r"C:\NBA Scraper\players\\" + player_name
        os.chdir(player_dir)
        write_headers(headers, filename)
        if URL[-9:] == 'playoffs/':
            stat_table = soup.find("table", { "id" : "pgl_basic_playoffs" })
            data = make_table_list(stat_table)
            write_rows(filename, data)   
            print("Finished File:   " + filename)
        else: 
            stat_table = soup.find("table", { "id" : "pgl_basic" })
            data = make_table_list(stat_table)
            write_rows(filename, data)
            print("Finished File:   " + filename)
        write_completed(log)
    else:            
        ncomp_counter += 1

'''Show Completion of Scraper'''
print("***SCRAPER HAS FINISHED***")
print("Completed: " + str(comp_counter) + " Files")
print("Ignored: " + str(ncomp_counter) + " URLS")
