import os
import json

filedirectory = 'historicaldata/'
filelist = os.listdir(filedirectory)


def e_utf(data):
        '''convert from unicode to string'''
        return data.encode("utf-8")


def intconv(data):
        '''convert blanks to zero'''
        if data.isdigit():
                return int(e_utf(data))
        else:
                return 0


def rounddata(data):
        rounds = {'R1': {}, 'R2': {}, 'R3':{}, 'R4':{}}
        for r in data:
                if e_utf(r['rndNum']) == 'Round 1':
                        rounds['R1'] = {'rndscore': intconv(r['rndScr']),\
                         'relparscr': intconv(r['relParScr']),\
                         'rndpos': e_utf(r['rndPos']),\
                         'cumparscr': intconv(r['cumParScr']),\
                         'coursenum': e_utf(r['courseNum'])}
                if e_utf(r['rndNum']) == 'Round 2':
                        rounds['R2'] = {'rndscore': intconv(r['rndScr']),\
                         'relparscr': intconv(r['relParScr']),\
                         'rndpos': e_utf(r['rndPos']),\
                         'cumparscr': intconv(r['cumParScr']),\
                         'coursenum': e_utf(r['courseNum'])}
                if e_utf(r['rndNum']) == 'Round 3':
                        rounds['R3'] = {'rndscore': intconv(r['rndScr']),\
                         'relparscr': intconv(r['relParScr']),\
                         'rndpos': e_utf(r['rndPos']),\
                         'cumparscr': intconv(r['cumParScr']),\
                         'coursenum': e_utf(r['courseNum'])}
                if e_utf(r['rndNum']) == 'Round 4':
                        rounds['R4'] = {'rndscore': intconv(r['rndScr']),\
                         'relparscr': intconv(r['relParScr']),\
                         'rndpos': e_utf(r['rndPos']),\
                         'cumparscr': intconv(r['cumParScr']),\
                         'coursenum': e_utf(r['courseNum'])}
        return rounds


def plyrdata(data):
        plyrdatadict = {}
        for plyr in data:
                plyrdatadict[e_utf(plyr['PlayerName'])] = {
                        'tournamentplyrid': e_utf(plyr['TournamentPlayerId']),\
                        'isalternate': e_utf(plyr['isAlternate']),\
                        'ismember': e_utf(plyr['isMember'])}
        return plyrdatadict


def tournsumplyrdata(data):
        plyrdatadict = {}
        for plyr in data:
                plyrdatadict[e_utf(plyr['plrNum'])] = {
                        'eventfedexpoints': intconv(plyr['EventFedExPoints']),\
                        'name': e_utf(plyr['name']['first'] + ' ' + plyr['name']['last']),\
                        'plyrname': e_utf(plyr['name']['last'] + ', ' + plyr['name']['first']),\
                        'totalscore': intconv(plyr['totScr']),\
                        'primarytour': e_utf(plyr['primaryTour']),\
                        'finposnum': intconv(plyr['finPos']['finPosNum']),\
                        'finposvalue': intconv(plyr['finPos']['finPosValue']),\
                        'money': intconv(plyr['money'].replace(',','')),\
                        'relparscrtot': intconv(plyr['relParScrTot']),\
                        'rounddata': rounddata(plyr['rnds'])}
        return plyrdatadict


def loadhistoricaldata():
        tournsum = {}
        field = {}
        setup = {}
        for f in filelist:
                if f.split('_')[2].split('.')[0] == 'tournsum':
                        year = f.split('_')[1]
                        tid = f.split('_')[0]
                        if tid not in tournsum.keys():
                                tournsum[tid] = {}
                        with open(filedirectory + f) as json_data:
                                try:
                                        d = json.load(json_data)
                                        for key in d.keys():
                                                if e_utf(key) == 'years':
                                                        if e_utf(d[key][0]['tours'][0]['tourName']) == 'PGA TOUR':
                                                                if e_utf(d[key][0]['tours'][0]['trns'][0]['shortName']) not in tournsum[tid].keys():
                                                                        tournsum[tid][e_utf(d[key][0]['tours'][0]['trns'][0]['shortName'])] = {}
                                                                tournsum[tid][e_utf(d[key][0]['tours'][0]['trns'][0]['shortName'])][int(year)] =\
                                                                        {'tournamentname': e_utf(d[key][0]['tours'][0]['trns'][0]['fullName']),\
                                                                        'players': tournsumplyrdata(d[key][0]['tours'][0]['trns'][0]['plrs'])
                                                                        }
                                except:
                                        continue

                if f.split('_')[2].split('.')[0] == 'field':
                        year = f.split('_')[1]
                        with open(filedirectory + f) as json_data:
                                try:
                                        d = json.load(json_data)
                                        for key in d.keys():
                                                if e_utf(key) == 'Tournament':
                                                        if e_utf(d[key]['TournamentPermId']) not in field.keys():
                                                                field[e_utf(d[key]['TournamentPermId'])] = {}
                                                        field[e_utf(d[key]['TournamentPermId'])][int(year)] = {\
                                                                'tournamentname': e_utf(d[key]['TournamentName']),\
                                                                't_id': e_utf(d[key]['T_ID']),\
                                                                'players': plyrdata(d[key]['Players'])}
                                except:
                                        continue

                if f.split('_')[2].split('.')[0] == 'setup':
                        year = f.split('_')[1]
                        if year not in setup.keys():
                                setup[year] = {}
                        with open(filedirectory + f) as json_data:
                                try:
                                        d = json.load(json_data)
                                        for key in d.keys():
                                                if e_utf(key) == 'trn':
                                                        setup[year][e_utf(d[key]['event']['name'])] = {'fieldsize': intconv(d[key]['event']['fieldSize']),\
                                                        'totalrnds': intconv(d[key]['event']['totalRnds'])}
                                                        for plyr in d[key]['field']:
                                                                setup[year][e_utf(d[key]['event']['name'])][e_utf(plyr['id'])] = \
                                                                        {'name': e_utf(plyr['name']['first'] + ' ' + plyr['name']['last']),\
                                                                        'plyrname': e_utf(plyr['name']['last'] + ', ' + plyr['name']['first']),\
                                                                        'money': {'ytdtotal': intconv(plyr['money']['ytdTotal']),\
                                                                        'ytdrank': intconv(plyr['money']['ytdRank']),\
                                                                        'ytdtrailing': intconv(plyr['money']['ytdTtrailing'])}}
                                except:
                                        continue

        return tournsum, field, setup
