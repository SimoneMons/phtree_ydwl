import requests
import re


url = 'https://www.youtube.com/watch?v=0_U4D3Wy-7k&list=RDEMDHx1mzcs_wPqWOntgHDScQ&index=5'
r = requests.get(url)
page_source = r.text

#print(page_source)
video_id_list = []

for m in re.finditer('":{"url":"/watch?', page_source):
   video_id = page_source[m.start() + 19:m.end() + 80]
   if 'index=' in video_id:
       print(video_id)
       video_id = video_id.split('\\')[0]
       if video_id not in video_id_list:
           video_id_list.append(video_id)


print(video_id_list)
#print(page_source)

