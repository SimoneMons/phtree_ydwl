import requests
import re
import urllib


url = 'https://www.youtube.com/watch?v=RB-RcX5DS5A&list=RDRB-RcX5DS5A&start_radio=1&t=7'
html = urllib.request.urlopen(url)
# print(html.read().decode())
s = html.read().decode()
s = s.replace('\n', '')

result = s.find('"playabilityStatus":{"status":"ERROR"')
print(result)

#"status":"ERROR" "playabilityStatus":{"status":"ERROR"
#print(page_source)

#print(page_source)
#video_id_list = []

'''
for m in re.finditer('":{"url":"/watch?', page_source):
   video_id = page_source[m.start() + 19:m.end() + 80]
   if 'index=' in video_id:
       print(video_id)
       video_id = video_id.split('\\')[0]
       if video_id not in video_id_list:
           video_id_list.append(video_id)


print(video_id_list)
#print(page_source)
'''
