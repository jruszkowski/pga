from __future__ import division
import sys
import urllib2
from bs4 import BeautifulSoup
from unicodedata import normalize
import mysql.connector
import scrape_field
import pandas as pd
import statsmodels.api as sm
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
	results = {unicode(x): (z, int(y)) for x,y,z in cursor}
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

def createdict(page):
   dict_page = {}
   page = urllib2.urlopen(page)
   soup = BeautifulSoup(page, "html5lib")
   right_table = soup.find('table', class_='table-styled')
   for row in right_table.findAll("tr"):
       cells = row.findAll('td')
       if len(cells) == 8:
           dict_page[cells[2].a.get_text()] = float(cells[4].string)
       if len(cells) == 7:
           dict_page[cells[2].a.get_text()] = float(cells[4].string)
   dict_page = {normalize('NFKC', k): v for k, v in dict_page.items()}
   return dict_page


def createplyrlist(page):
   plyrlist = []
   page = urllib2.urlopen(page)
   soup = BeautifulSoup(page, "html5lib")
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
	plot_rows = ceil(len(stats.keys()) / 2)
	fig = Figure()
	fig.set_size_inches(11.5, 36)
	canvas = FigureCanvasAgg(fig)
	subplot = 1
	stat_tscore = {}
        for i in stats.keys():
           	page = pagename + str(i) + '.' + year + pagenameend
		try:
			df[i] = pd.DataFrame.from_dict(createdict(page), orient='index')
			df_test = df[[i, 'Past Score']].dropna(how='any')
			ax = fig.add_subplot(plot_rows, 2, subplot)
			ax.set_title(stats[i])
			ax.scatter(df_test['Past Score'].tolist(), df_test[i].tolist())
			subplot+=1
			y = df_test['Past Score'].dropna().tolist()
			x = df_test[i].dropna().tolist()
			x = sm.add_constant(x)
			model = sm.OLS(y, x)
			results = model.fit()
			stat_tscore[stats[i]] = results.tvalues[1]
		except:
			print stats[i], i, ' No good'
			continue
	canvas.print_png('images/' + plot + '.png')
	df_tscore = pd.DataFrame.from_dict(stat_tscore, orient='index')	
	df_tscore.columns = ['tscore']
	df_tscore['tscore_abs'] = df_tscore['tscore'].abs()
	print (plot, df_tscore.sort_values('tscore_abs', ascending=False).head(10))


if __name__=='__main__':
	shortname = sys.argv[1]
	year = sys.argv[2]
	f,c = get_scores(year, shortname)
	print (scipy.stats.describe(f.values()))
	print (scipy.stats.describe(c.values()))
	for past_results in [f, c]:
		create_images(past_results)
