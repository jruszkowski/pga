from __future__ import division
import sys
import urllib.request
from bs4 import BeautifulSoup
from unicodedata import normalize
import mysql.connector
import scrape_field
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as sm2
import scipy
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from math import ceil

pagename = "http://www.pgatour.com/stats/stat."
pagenameend = ".html"

cnx = mysql.connector.connect(user='root', password='',
                              host='130.211.169.146',
                              database='pga')

def get_scores(year, shortname):
    cursor=cnx.cursor()
    query = ("select plyr_name, \
                    totalscore, \
                    finposnum \
                    from tournsum where year = '%s' \
                                    and shortname = '%s' \
                                    and totalscore > 120;" % (year, shortname))
    cursor.execute(query)
    results = {x: (z, int(y)) for x,y,z in cursor}
    cursor.close()
    cnx.close()
    finisher_results = {x: y[1] for x,y in results.items() if y[0] < 999 and y[1] > 240}
    cut_results = {x: y[1] for x,y in results.items() if y[0] == 999}
    return finisher_results, cut_results


stats = {
102: 'ACCURATE',
103: 'GIR',
111: 'SAND',
112: 'BIRD_3',
113: 'BIRD_4',
114: 'BIRD_5',
119: 'PUTTS',
120: 'SCORE',
129: 'DRIVE',
#138: 'TOP10',
142: 'PAR3',
143: 'PAR4',
144: 'PAR5',
145: 'PUTT3',
146: 'PUTT3_20',
147: 'PUTT3_25',
156: 'B_AVG',
158: 'STRIKE',
#187: 'PRESIDENTS',
190: 'GIR_F',
209: 'LOW',
213: 'FAIRWAY',
214: 'D300',
215: 'D280',
216: 'D260',
217: 'D240',
218: 'D220',
326: 'GIR_200',
327: 'GIR_175',
328: 'GIR_150',
329: 'GIR_125',
330: 'GIR_100',
#351: 'HOLE_OUT',
352: 'BIRD',
399: 'PUTT2',
459: 'LEFT',
460: 'RIGHT',
461: 'MISSED',
467: 'SCRAM'
}

def createdict(url):
   dict_page = {}
   request = urllib.request.Request(url)
   response = urllib.request.urlopen(request)
   soup = BeautifulSoup(response, "lxml")
   right_table = soup.find('table', class_='table-styled')
   for row in right_table.findAll("tr"):
       cells = row.findAll('td')
       if len(cells) == 8:
           dict_page[cells[2].a.get_text()] = float(cells[4].string)
       if len(cells) == 7:
           dict_page[cells[2].a.get_text()] = float(cells[4].string)
   return dict_page


def createplyrlist(url):
   plyrlist = []
   request = urllib.request.Request(url)
   response = urllib.request.urlopen(request)
   soup = BeautifulSoup(response, "lxml")
   right_table = soup.find('table', class_='table-styled')
   for row in right_table.findAll("tr"):
       cells = row.findAll('td')
       if len(cells) == 8:
           plyrlist.append(cells[2].a.get_text())
   return plyrlist


def create_images(past_results):
    df = pd.DataFrame.from_dict(past_results, orient='index')
    df.columns = ['Past Score']
    plot = 'made_cut'
    if df['Past Score'].mean() < 200:
            plot = 'cut'
    stat_tscore = {}
    for i in stats.keys():
        page = pagename + str(i) + '.' + year + pagenameend
        try:
            df[i] = pd.DataFrame.from_dict(createdict(page), orient='index')
            df_test = df[[i, 'Past Score']].dropna(how='any')
            y = df_test['Past Score'].dropna().tolist()
            x = df_test[i].dropna().tolist()
            x = sm.add_constant(x)
            model = sm.OLS(y, x)
            results = model.fit()
            stat_tscore[stats[i]] = results.tvalues[1]
        except:
            print (stats[i], i, ' No good')
            continue
    df_tscore = pd.DataFrame.from_dict(stat_tscore, orient='index')	
    df_tscore.columns = ['tscore']
    df_tscore['tscore_abs'] = df_tscore['tscore'].abs()
    df_tscore['key_value'] = pd.Series({v: k for k, v in stats.items()})
    print (df_tscore.sort_values('tscore_abs', ascending=False).head(10))

def get_ols(past_results, get_params=False):
    ind_var = [114, 217, 113, 119, 216, 399]
    df = pd.DataFrame.from_dict(past_results, orient='index')
    for stat in ind_var:
        page = pagename + str(stat) + '.' + str(year) + pagenameend
        try:
           df[stats[stat]] = pd.DataFrame.from_dict(createdict(page), orient='index')
        except:
           print(stats[stat], 'No good')
           continue
    df = df.rename(columns={0:'Result'})
    result = sm2.ols(formula="Result ~ BIRD_5 + D240 + BIRD_4 + PUTTS + D260 + PUTT2", data=df).fit()
    if get_params:
        return (result.params.to_dict())
    print (result.summary())


def get_predicted_score(d_params):
    ind_var = [114, 217, 113, 119, 216]
    new_field = []
    new_field_dict = scrape_field.field_dictionary()
    for key in new_field_dict.keys():
        for plyr in new_field_dict[key]['players'].keys():
                new_field.append(plyr)
    new_field = [x.split(',')[1].strip() + ' ' + x.split(',')[0] for x in new_field]

    df = pd.DataFrame(new_field)
    df = df.rename(columns={0: 'PredictedScore'})
    df = df.set_index('PredictedScore')
    for stat in ind_var:
       page = pagename + str(stat) + '.' + pagenameend
       try:
           df[stats[stat]] = pd.DataFrame.from_dict(createdict(page), orient='index')
       except:
           print (stats[stat], 'No good')
           continue

    df['Prediction'] = d_params['Intercept'] \
            + d_params['BIRD_5'] * df['BIRD_5'] \
            + d_params['D240'] * df['D240'] \
            + d_params['BIRD_4'] * df['BIRD_4'] \
            + d_params['PUTTS'] * df['PUTTS'] \
            + d_params['D260'] * df['D260'] \
#    df = df['Prediction']
    df.to_csv('pga.csv')

    return df.to_dict()

if __name__=='__main__':
    shortname = sys.argv[1]
    year = sys.argv[2]
    f,c = get_scores(year, shortname)
    print (scipy.stats.describe(list(f.values())))
    #print (scipy.stats.describe(list(c.values())))
    create_images(f)
    get_ols(f)
    get_predicted_score(get_ols(f, True))
    #get_predicted_score(get_ols(c, True))
    #for past_results in [f, c]:
    #	create_images(past_results)
