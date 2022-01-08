# python3 -m pip install beautifulsoup4
# python3 -m pip install requests
# python3 -m pip install json
# python3 -m pip install lxml

from bs4 import BeautifulSoup
import requests, json, lxml

site = 'datastax.com'
query = 'data lineage'

# # creating a list of all common heading tags
# heading_tags = ["h1", "h2", "h3"]
# for tags in soup.find_all(heading_tags):
#     print(tags.name + ' -> ' + tags.text.strip())

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

## Visit SERP linked pages and get data

pos = 0

for page in pages:
  html = requests.get(pages[pos], headers=headers)
  soup = BeautifulSoup(html.text, 'lxml')

  title = soup.select_one('title')

  for result in soup.select('title,h1,h2'):
    data.append('Page~'+pages[pos]+'~'+result.name+'~'+result.text.strip())    

  # break
  pos += 1


print("\n".join(data))
# print(json.dumps(pages, indent=2, ensure_ascii=False))