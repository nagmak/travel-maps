#! python3

import requests, os, bs4

url = 'http://xkcd.com'
os.makedirs('xkcd', exist_ok=True) #store comics in ./xkcd

while not url.endswith('#'):
    
    # LOADS XKCD home page/Download page with requests module
    print('Downloading page %s...' % url)
    
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)
    
    # SAVES comic image on that page/Find url of comic with beautiful soup
    comicElem = soup.select('#comic img')
    
    if comicElem == []:
        print('Could not find comic image.')
    else:
        try:
            comicUrl = 'http:' + comicElem[0].get('src')
            
            print('Downloading image %s...' % (comicUrl))
            
            res = requests.get(comicUrl)
            res.raise_for_status()
            
        except requests.exceptions.MissingSchema:
            
            #skip comic
            prevLink = soup.select('a[rel="prev"]')[0]
            url = 'http://xkcd.com' + prevLink.get('href')
            continue
        
    # FOLLOWS previous comic link/download and save w iter_content()
    imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')

    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
    
    # REPEAT until it reaches the first comic
    prevLink = soup.select ('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')
    
print('Done.')
