import urllib2
from bs4 import BeautifulSoup

field = "http://www.pgatour.com/data/r/"
filedirectory = 'historicaldata/'
jsonfiles = ['setup', 'tournsum', 'teetimes', 'course', 'field']

def getjson(page):
    page = urllib2.urlopen(page)
    soup = BeautifulSoup(page)
    return soup.get_text()

tourneyids = [
'040', '023', '045', '004', '035', '457', '010', '054',
'012', '013', '058', '016', '019', '018', '033', '030',
'031', '100', '034', '493', '472', '056', '518', '483',
'051', '002', '650', '037', '032', '505', '060', '088',
'468', '005', '464', '025', '024', '001', '026', '021',
'020', '489', '022', '047', '009', '008', '029', '028',
'041', '480', '003', '494', '011', '027', '519', '473',
'470', '471', '476', '014', '475', '007', '478', '006',
'490'
]

years = list(range(2000,2018))

for tourneyid in tourneyids:
    for year in years:
        for json in jsonfiles:
            try:
                print field+tourneyid+'/'+str(year)+'/' + json + '.json'
                jsondata = getjson(field+tourneyid+'/'+str(year)+'/' + json + '.json')
                if len(jsondata) > 0:
                    with open(filedirectory+tourneyid+'_' + str(year) + '_' + json + '.txt', 'w') as f:
                        f.write(jsondata)
            except:
                print 'no good', tourneyid
                continue
