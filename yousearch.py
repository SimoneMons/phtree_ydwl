from youtubesearchpython import SearchVideos, SearchPlaylists
import json

search = SearchVideos("bella cosa", offset = 1, mode = "json", max_results = 20)

#search = SearchPlaylists("cold play", offset = 1, mode = "json", max_results = 20)

#print(search.result())


aaa = json.loads(search.result())

bbb = aaa['search_result']

for d in bbb:
    print(d['id'])

print(bbb)


# Search all the companies code recorded in the system
'''
company_details = []
for data_dict in search.result:
            for key in data_dict:
                if key == 'link':
                    print(data_dict[0])


import os
import re

import youtube_dl

# Global variables
SAVE_PATH = os.path.expanduser('~/Downloads')

ydl_video = {
    'format': 'best',
    'dumpjson': True,
    'outtmpl': SAVE_PATH + '/_video/%(title)s.%(ext)s',
}

ydl_audio = {
    'format': 'bestaudio/best',
    'outtmpl': SAVE_PATH + '/_audio/%(title)s.%(ext)s',
}

dwl_link = 'https://www.youtube.com/playlist?list=PL00176FD3DE99A115'

list_id = ''

#if 'list' in dwl_link:
#    list_id = re.search(r'list=(.*?)&', dwl_link).group(1)
#    print(list_id)

with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
    ydlvideo.download(['https://www.youtube.com/playlist?list=PL00176FD3DE99A115'])
'''
