import psycopg2 as psy
import re
import csv
import matplotlib.pyplot as plt
import numpy

con = psy.connect('dbname=daproject user=myuser')
cur = con.cursor()
cur.execute('select text from twitter.totaltweets;')
texts = cur.fetchall()

#gets all 32 NFL teams in list
teamscsv = open('teamlist.csv','rU')
csvfile = csv.reader(teamscsv)
teamlist = []
for i in range(0,32):
    teamlist.append(csvfile.next()[0])

#lists of lists, each list in the list has city and team name
teamsncities = [i.split() for i in teamlist]
teamsncities[8] = ['St. Louis', 'Rams']
teamsncities[27] = ['Tampa Bay', 'Buccaneers']
teamsncities[24] = ['New Orleans', 'Saints']
teamsncities[17] = ['New England', 'Patriots']
teamsncities[16] = ['New York', 'Jets']
teamsncities[14] = ['San Diego', 'Chargers']
teamsncities[13] = ['Kansas City', 'Chiefs']
teamsncities[9] = ['San Francisco', '49ers']
teamsncities[2] = ['Green Bay', 'Packers']
teamsncities[3] = ['New York', 'Giants']
teamsncities.pop(13)
teamsncities.pop(2)

#gets number of times the string appears in the text
def get_count(string, text):
    mentions = re.findall(string, text, re.IGNORECASE)
    return len(mentions)

teams = [i[0] for i in teamsncities]
cities = [i[1] for i in teamsncities]


A = {}
for i in teamsncities:
    A[i[1]] = 0
    for j in texts:
        sofar = get_count(i[0], j[0])
        A[i[1]] += sofar
        sofar2 = get_count(i[1], j[0])
        A[i[1]] += sofar2


#so now we have a dictionary of all 32 teams and the number of times they were mentioned in the tweets we scraped

teamnames = A.keys()
counts = [A[i] for i in teamnames]
splits = range(2,62, 2)

fig, ax = plt.subplots()
ax.bar(splits, counts, width=2, align = 'center', color='c')
ax.set_xticks(splits)
ax.set_xticklabels(teamnames, rotation = 60)
ax.set_title('Teams Names and Cities From Twitter Text')
plt.ylabel('Times Names and Cities Found in Text')
plt.savefig('slide.png')
