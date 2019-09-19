import sqlite3
from discord.utils import find
import datetime
from operator import itemgetter

def topusers(month, channel):

    
    conn = sqlite3.connect("gametime.db")
    
    cursor = conn.execute('select ID from '+month) # get all user ids
    users = [user[0] for user in cursor.fetchall()]

    cursor = conn.execute('select * from '+month)
    games = [game[0] for game in cursor.description] #get list of games
    games.pop(0) 


    totals = [0]*len(users)
    
    for i in range(len(users)):
        for game in games:
            cursor = conn.execute('select '+game+' from '+month+' where ID = '+users[i])
            totals[i] += cursor.fetchone()[0] # sums up the times for each user
        
        


    totals = map(lambda x: x/3600, totals)

    user_totals = list(zip(users,totals))
    user_totals = [i for i in user_totals if i[0] != "Spotify" ] # remove spotify
    user_totals = sorted(user_totals,key=itemgetter(1), reverse = True) # sorts the list in descending order

    #begin constructing message

    message = "Top %s gamerz in %s:\n```" % ("10", month.lower())

   
    user_totals = user_totals[:10] # only displays the number of games desired

    for user in user_totals:

        member = find(lambda m: m.id == user[0], channel.server.members)
        message += '%s - {0:.2f} hours\n\n'.format(user[1]) % member.display_name


    message += '```'

    
    return message
