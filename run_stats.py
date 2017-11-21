from __future__ import division
import sys
import urllib2
from bs4 import BeautifulSoup
from unicodedata import normalize
import mysql.connector
import scrape_field
import pandas as pd
import statsmodels.formula.api as sm


pagename = "http://www.pgatour.com/stats/stat."
pagenameend = ".html"

cnx = mysql.connector.connect(user='root', password='',
                              host='130.211.169.146',
                              database='pga')

def get_scores(year, shortname):
	cursor=cnx.cursor()
	query = ("select plyr_name, totalscore, finposnum from tournsum where year = '%s' and shortname = '%s';" % (year, shortname))
	cursor.execute(query)
	finisher_results = {x: int(y) for x,y,z in cursor if z < 999}
	cut_results = {x: int(y) for x,y,z in cursor if z == 999}
	cursor.close()
	cnx.close()
	return finisher_results, cut_results


if __name__=='__main__':
	shortname = sys.argv[1]
	year = sys.argv[2]
	get_scores()
