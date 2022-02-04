# python3 -m pip install beautifulsoup4
# python3 -m pip install requests
# python3 -m pip install json
# python3 -m pip install lxml
# python3 -m pip install pyperclip

# to run: python3 scraper.py 'your query' 'somesite.com'

# https://docs.google.com/spreadsheets/d/1QFTquIG2ek-TIPIl0a5xSGBiGNvVjnwpDbizJnaBQ-0/edit#gid=0

from bs4 import BeautifulSoup
import requests, json, lxml, pyperclip, sys, re

query = sys.argv[1]
site = sys.argv[2]

headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

## Get first SERP

params = {
  'q': query,  # query 
  'gl': 'us',    # country to search from
  'hl': 'en',    # language
  'num': 20
}

html = requests.get("https://www.google.com/search", headers=headers, params=params)
soup = BeautifulSoup(html.text, 'lxml')

# Parse top pages

data = []
pages = []
pos = 0

for result in soup.select('.tF2Cxc'):
  pos += 1
  title = result.select_one('.DKV0Md').text
  link = result.select_one('.yuRUbf a')['href']

  # sometimes there's no description and we need to handle this exception
  try: 
    snippet = result.select_one('#rso .lyLwlc').text
  except: snippet = 'None'

  data.append('Result~'+str(pos)+'~Title~'+title)
  data.append('Result~'+str(pos)+'~Link~'+link)
  data.append('Result~'+str(pos)+'~Snippet~'+snippet)

  pages.append(link)

# Parse PAA

pos = 0

for result in soup.select('.iDjcJe'):
  pos += 1
  title = result.select_one('span').text
  data.append('PAA~'+str(pos)+'~Title~'+title)

# Parse Related

pos = 0

for result in soup.select('.s75CSd'):
  pos += 1
  text = result.text

  data.append('Related~'+str(pos)+'~Text~'+text)

## Visit SERP linked pages and get data

pos = -1

for page in pages:
  pos += 1
  try:
    if pages[pos].endswith('pdf'):
      raise Exception("An exception occurred on "+pages[pos])
      continue
    html = requests.get(pages[pos], headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    for result in soup.select('title,h1,h2,h3,strong'):
      s = result.get_text()
      s = re.sub(r'[^a-zA-Z0-9]', ' ', s)
      s = ' '.join(s.split())
      data.append('Page~'+pages[pos]+'~'+result.name+'~'+s)    

  except:
    print("An exception occurred on "+pages[pos])

## Get SERP for on-site pages

pos = 0

params = {
  'q': query + ' site:' + site,  # query 
  'gl': 'us',    # country to search from
  'hl': 'en',    # language
  'num': 10
}

html = requests.get("https://www.google.com/search", headers=headers, params=params)
soup = BeautifulSoup(html.text, 'lxml')

# Parse results

for result in soup.select('.tF2Cxc'):
  pos += 1
  title = result.select_one('.DKV0Md').text
  link = result.select_one('.yuRUbf a')['href']

  # sometimes there's no description and we need to handle this exception
  try: 
    snippet = result.select_one('#rso .lyLwlc').text
  except: snippet = 'None'

  data.append('Post~'+str(pos)+'~Title~'+title)
  data.append('Post~'+str(pos)+'~Link~'+link)
  data.append('Post~'+str(pos)+'~Snippet~'+snippet)

  pages.append(link)

## Clean up and print, copy to clipboard

data = list(dict.fromkeys(data))

print("\n".join(data))
pyperclip.copy("\n".join(data))
# print(json.dumps(pages, indent=2, ensure_ascii=False))
