
import urllib.request
import urllib.parse
import io
import re

import requests
from bs4 import BeautifulSoup


'''with urllib.request.urlopen('https://www.youtube.com/watch?list=RDEMDHx1mzcs_wPqWOntgHDScQ') as response:
   html = response.read()

print(html)
'''

#print(html)


vgm_url = 'https://m.youtube.com/playlist/?list=RDEMDHx1mzcs_wPqWOntgHDScQ'
html_text = requests.get(vgm_url).text
print(html_text)


'''
with io.open('myfile.txt', "w", encoding="utf-8") as f:
   f.write(html_text)

# \n is placed to indicate EOL (End of Line)


open('myfile.txt', 'r', encoding="utf-8").read().find('aa')

start = '"watchEndpoint":{"videoId":"'
end = '"}},'

#"watchEndpoint":{"videoId":"yyaMYcOxdqM"}},

searchfile = open('myfile.txt', 'r', encoding="utf-8")


for line in searchfile:
   if "watchEndpoint" in line:
      result = re.search(r'watchEndpoint(.*?)ownerText', line).group(1)
      print(result)



#print(html_text)
result = re.search(r'watchEndpoint(.*?)ownerText', html_text).group(1)
#print(result)

video_id_list = []

for m in re.finditer('watchEndpoint', html_text):
   video_id = html_text[m.start() + 27:m.end() + 25]
   video_id_list.append(video_id)
   #print(html_text[m.start() + 26:m.end() + 26])
   #print('Found in ', m.start(), m.end())

print(video_id_list)

#'"hG4lT4fxj8M"'
searchfile.close()
'''

