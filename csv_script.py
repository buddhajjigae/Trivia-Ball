import csv
import os
import pathlib
import pymysql
import pandas as pd
from os import path


#########################################################
'''                      METHODS                      ''' 
#########################################################

def get_player_id(file):
    counter = 0
    
        if i == 
        

def write_csv(filename, data):
    with open(filename, 'a') as csvfile:  
            writer = csv.writer(csvfile, delimiter = ',')
            i = 0
            for e in data:
                writer.writerow(data[0+i]) 
                i += 1


def write_completed(url):
    with open(r'C:\NBA Scraper\Fixed_Completed.txt', 'a') as txtfile:
        txtfile.write(url + "\n")


def write_files_toFix(files):
    with open(r"C:\NBA Scraper\File_Log.txt", "a") as textfile:
        for file in files:
            textfile.write(file + "\n")
                
#########################################################
'''                    MAIN CODE                      ''' 
#########################################################

'''Creating Necessary Files'''
if path.exists(r"C:\NBA Scraper\Fixed_Completed.txt") == False:
    os.chdir(r"C:\NBA Scraper\\")
    comp_file = open('Fixed_Completed.txt','w')
    comp_file.close()
    print("Created Fixed_Completed.txt")
else:
    print(r"C:\NBA Scraper\Fixed_Completed.txt   File Exists, Will Not Create File")
    
    
if path.exists(r"C:\NBA Scraper\File_Log.txt") == False:
    os.chdir(r"C:\NBA Scraper\\")
    comp_file = open('File_Log.txt','w')
    comp_file.close()
    print("Created File_Log.txt")
else:
    print(r"C:\NBA Scraper\File_Log.txt   File Exists, Will Not Create File")


'''SQL Database Connection'''
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='buddhajjigae',
                             db='nba_scraper',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor_sql = connection.cursor()

'''Column Names for SQL Table'''
c1 = "ranker INT, game_season INT, date_game TEXT, age TEXT, team_id TEXT,"
c2 = "game_location TEXT, opp_id TEXT, game_result TEXT, gs TEXT, mp TEXT,"
c3 = "fg INT, fga INT, fg_pct DOUBLE, fg3 INT, fg3a INT, fg3_pct DOUBLE,"
c4 = "ft INT, fta INT, ft_pct DOUBLE, orb INT, drb INT, trb INT, ast INT,"
c5 = "stl INT, blk INT, tov INT, pf INT, pts INT, game_score DOUBLE,"
c6 = "plus_minus TEXT, player_id VARCHAR(20), playoff TEXT);"
c_names = "CREATE TABLE `nba_scraper`.`players` (" + c1 + c2 + c3 + c4 + c5 + c6


'''Make player_id a primary key'''
p_key = "ALTER TABLE players ADD PRIMARY KEY (player_id);"

'''Insert row into db'''
sql_1 = "INSERT INTO players (ranker, game_season, date_game, age, team_id, "  
sql_2 = "game_location, opp_id, game_result, gs, mp, fg, fga, fg_pct, fg3, "
sql_3 = "fg3a. fg3_pct, ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, tov "
sql_4 = "pf, pts, game_score, plus_minus, player_id, playoff) VALUES "
sql_5 = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
sql_6 = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"       
sql = sql_1 + sql_2 + sql_3 + sql_4 + sql_5 + sql_6

'''Check if players table exists in DB'''
with connection.cursor() as cursor:
        # Create a new record
        sql = "SHOW TABLES LIKE 'players'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            print('Players table exists in SQL DB, will not create table.')
        else:
            cursor.execute(c_names)
            cursor.execute(p_key)
            print('Players table created in SQL DB')    


#directory = r'C:\NBA Scraper\players'

'''Files in directory'''
file_list = []

'''Already completed files'''
comp_files_raw = []
comp_files = []

'''name_types are the 'Did Not Play, Inactive, etc.'''
name_types_list = []
name_types_set = []


# '''Files that have been completed'''
# clean_comp = []

'''
for file in os.listdir(directory):
    file_list.append(file + ".csv")
'''

for path_a, subdirs, files in os.walk(r'C:\NBA Scraper\players'):
    for name in files:
        file_path = str(pathlib.PurePath(path_a, name))        
        file_list.append(file_path)
        
print(len(file_list))

with open(r'C:\NBA Scraper\Fixed_Completed.txt', 'r') as comp_file:
    comp_files_raw = comp_file.readlines()

for file in comp_files_raw:
    file = file.replace('\n','')
    comp_files.append(file)

print(comp_files)    

'''Counters'''
clean_count = 0
no_count = 0    

for file in file_list:    
    raw_list = []
    fixed_list = []   
    
    for e in file:      
    if file not in comp_files and file[-8:] != 'Test.csv':
        clean_count += 1
        playoffs = file[-14:-4]
        with open(file, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')                      
                for row in csv_reader:
                    if len(row) != 0:
                        raw_list.append(row)                                    
                for i in raw_list:
                    for j,e in enumerate(i):
                        if i[j] == '' and j != 5:
                            i[j]= 'NULL'                              
                        elif e == 'Did Not Play':
                            i.extend(['NULL'] * 21)
                        elif e == 'Did Not Dress':
                            i.extend(['NULL'] * 21)
                        elif e == 'Player Suspended':
                            i.extend(['NULL'] * 21)
                        elif e == 'Inactive':
                            i.extend(['NULL'] * 21)
                        elif e == 'Not With Team':
                            i.extend(['NULL'] * 21)                                                 
                        name_types_list.append(i[8])                                       
                    if playoffs == 'playoffs':
                        i.extend('Yes')
                    else:
                        i.extend('No')
                    cursor_sql.execute(sql, i)
                    #pd_list = pd_list.append(i)
                    #df = pd.DataFrame(i)
                    #print(df)
                    fixed_list.append(i)
                    #print('FILE DONE: ' + file) 
    else:
        no_count += 1           
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))           
                          
# name_types_set = set(name_types_list)
# name_types_list = list(name_types_set)
# print(name_types_list)      
# print("***CLEANER HAS FINISHED***")
# print("Cleaned: " + str(clean_count) + " Files")
# print("Ignored: " + str(no_count) + " Files")
