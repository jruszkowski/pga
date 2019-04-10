#!urs/bin/python3

from bs4 import BeautifulSoup
import json
import requests
from collections import defaultdict



def e_utf(data):
        '''convert from unicode to string'''
        return data.encode("utf-8")

def intconv(data):
        '''convert blanks to zero'''
        if data.isdigit():
                return int(e_utf(data))
        else:
                return 0

def plyrdata(data):
    plyrdatadict = {}
    for plyr in data:
        plyrdatadict[plyr['PlayerName']] = {
                'tournamentplyrid': plyr['TournamentPlayerId'],\
                'isalternate': plyr['isAlternate'],\
                'ismember': plyr['isMember']}
    return plyrdatadict

def field_dictionary():
    field = "https://statdata.pgatour.com/r/current/field.json"
    response = requests.get(field)
    d = response.json()
    field = defaultdict(dict) 
    for key in d.keys():
        if key == 'Tournament':
            field[d[key]['TournamentPermId']] = {\
                    'tournamentname': d[key]['TournamentName'],\
                    't_id': d[key]['T_ID'],\
                    'players': plyrdata(d[key]['Players'])}

    return field
