import urllib.request
url = "https://cdn.discordapp.com/attachments/930209527306018888/937831833339580436/61df23528fe89.image.jpg"
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }

req = urllib.request.Request(url, headers=hdr)
response = urllib.request.urlopen(req)
response.read()