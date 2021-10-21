import urllib.request 
from bs4 import BeautifulSoup

field = "http://www.pgatour.com/data/r/"
field_v2 = "https://statdata.pgatour.com/r/"
filedirectory = 'historicaldata/'
jsonfiles = ['setup', 'tournsum', 'teetimes', 'course', 'field']

def getjson(page):
    request = urllib.request.Request(page)
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response)
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

years = list(range(2017,2022))

for tourneyid in tourneyids:
    for year in years:
        for json in jsonfiles:
            try:
                if year < 2018:
                    address = field
                else:
                    address = field_v2
                print (address+tourneyid+'/'+str(year)+'/' + json + '.json')
                jsondata = getjson(address+tourneyid+'/'+str(year)+'/' + json + '.json').encode('utf-8').strip()
                if len(jsondata) > 0:
                    with open(filedirectory+tourneyid+'_' + str(year) + '_' + json + '.txt', 'wb') as f:
                        f.write(jsondata)
            except:
                print ('no good', tourneyid)
                continue
