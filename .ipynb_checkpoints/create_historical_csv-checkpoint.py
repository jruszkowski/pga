import loaddata as ld
import csv
import pandas as pd

tournsum, field, setup = ld.loadhistoricaldata()

tourneylist = []
i = 1
for key in tournsum.keys():
    for shortname in tournsum[key].keys():
        for year in tournsum[key][shortname].keys():
            for plyr in tournsum[key][shortname][year]['players'].keys():
                tourneylist.append([i, key, shortname, year, plyr,\
                tournsum[key][shortname][year]['players'][plyr]['finposvalue'],\
                tournsum[key][shortname][year]['players'][plyr]['primarytour'],\
                tournsum[key][shortname][year]['players'][plyr]['name'],\
                tournsum[key][shortname][year]['players'][plyr]['money'],\
                tournsum[key][shortname][year]['players'][plyr]['finposnum'],\
                tournsum[key][shortname][year]['players'][plyr]['totalscore'],\
                tournsum[key][shortname][year]['players'][plyr]['eventfedexpoints'],\
                tournsum[key][shortname][year]['players'][plyr]['plyrname'],\
                tournsum[key][shortname][year]['players'][plyr]['relparscrtot']])
                i+=1

df = pd.DataFrame(tourneylist)
df = df.set_index([0])
df.to_csv('table_data/tournament_plyr.csv', header=False)


tourneylist2 = []
i=1
for key in tournsum.keys():
    for shortname in tournsum[key].keys():
        for year in tournsum[key][shortname].keys():
            tourneylist2.append([i, key, shortname, year, tournsum[key][shortname][year]['tournamentname']])
            i+=1

df = pd.DataFrame(tourneylist2)
df = df.set_index([0])
df.to_csv('table_data/tournament_tabler.csv', header=False)


round1 = []
round2 = []
round3 = []
round4 = []
for key in tournsum.keys():
    for shortname in tournsum[key].keys():
        for year in tournsum[key][shortname].keys():
            for plyr in tournsum[key][shortname][year]['players'].keys():
                if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1'].keys():
                    round1.append([key, shortname, year, plyr, 1,\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['rndscore'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['relparscr'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['rndpos'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['cumparscr'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R1']['coursenum']])

                if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2'].keys():
                    round2.append([key, shortname, year, plyr,2,\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['rndscore'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['relparscr'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['rndpos'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['cumparscr'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R2']['coursenum']])

                if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3'].keys():
                    round3.append([key, shortname, year, plyr, 3,\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['rndscore'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['relparscr'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['rndpos'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['cumparscr'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R3']['coursenum']])

                if 'rndscore' in tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4'].keys():
                    round4.append([key, shortname, year, plyr, 4,\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['rndscore'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['relparscr'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['rndpos'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['cumparscr'],\
                    tournsum[key][shortname][year]['players'][plyr]['rounddata']['R4']['coursenum']])

rounds = {'R1':round1,'R2':round2,'R3':round3,'R4':round4}

for r in rounds.keys():
    with open('table_data/' + r + '.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(rounds[r])
