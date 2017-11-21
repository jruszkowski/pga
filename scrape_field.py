import urllib2
from bs4 import BeautifulSoup
import json
import requests



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
                plyrdatadict[e_utf(plyr['PlayerName'])] = {
                        'tournamentplyrid': e_utf(plyr['TournamentPlayerId']),\
                        'isalternate': e_utf(plyr['isAlternate']),\
                        'ismember': e_utf(plyr['isMember'])}
        return plyrdatadict

def field_dictionary():
        field = "http://www.pgatour.com/data/r/current/field.json"
        response = requests.get(field)
        d = response.json()
        field = {}
        for key in d.keys():
                if e_utf(key) == 'Tournament':
                        if e_utf(d[key]['TournamentPermId']) not in field.keys():
                                field[e_utf(d[key]['TournamentPermId'])] = {}
                        field[e_utf(d[key]['TournamentPermId'])] = {\
                                'tournamentname': e_utf(d[key]['TournamentName']),\
                                't_id': e_utf(d[key]['T_ID']),\
                                'players': plyrdata(d[key]['Players'])}

        return field
