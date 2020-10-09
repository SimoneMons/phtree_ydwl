import urllib.request
import urllib.parse
import io
import re
import csv
import json

import requests

# from bs4 import BeautifulSoup


'''with urllib.request.urlopen('https://www.youtube.com/watch?list=RDEMDHx1mzcs_wPqWOntgHDScQ') as response:
   html = response.read()

print(html)
'''

# print(html)


html = urllib.request.urlopen("http://thenostalgiamachine.com/js/years.min.js")
# print(html.read().decode())
s = html.read().decode()
s = s.replace('\n', '')

# print(s)

dict_of_songs = {} #id: {'year': '', 'singer': '', 'title': '', 'link': ''}}


list_of_years = []
list_of_songs_for_year = []

# years = re.findall('(?<=_)\d{4}(=songs)', s)
years = re.findall(r'\_(\d{4})\={songs', s)
for year in years:
    list_of_years.append((year))

ccc = ''

for year in list_of_years:
    left_identifier = '_' + str(year) + '={songs:['
    right_identifier = ']},_' + str(int(year) + 1) + '={songs:'
    if year == max(list_of_years):
        right_identifier = ']]};'
    sss = "{}(.*?){}".format(*map(re.escape, (left_identifier, right_identifier)))
    # print(sss)
    songs = re.findall(sss, s)
    # print(year)
    # print(songs)
    songs_string = str(songs)
    # print(aaa[2:-2])
    songs_string = songs_string[2:-2]
    # print(year)
    # print(songs_string)
    songs_string_1 = songs_string.split('],[')
    #print(year)
    for i in range(0, len(songs_string_1)):


        songs_string_2 = songs_string_1[i].split(',')
        #print(songs_string_2[1])

        #dict_of_songs['Id'] = i
        dict_of_songs['year'] = year
        dict_of_songs['singer'] = songs_string_2[0].replace('[', '')
        dict_of_songs['title'] = songs_string_2[1]
        dict_of_songs['link'] = songs_string_2[2]
        list_of_songs_for_year.append(dict_of_songs.copy())


       #dict_of_songs = dict_of_songs + dict_of_songs_help

        # dict_of_songs.setdefault(year, []).append(songs)

        # print(songs_string_2[0].replace('[', ''))
        # print(songs_string_2[1])
        # print(songs_string_2[2])
    # print(year)
    # print(bbb)
    # list_of_songs_for_year.append(year)
    # li = list(songs_string.split('],['))
    # list_of_songs_for_year.append(li)
    '''
    bbb1 = bbb.replace('[', '')
    bbb2 = bbb1.replace(']', '')
    bbb4 = bbb2.replace('"', '')
    bbb4 = year + ',' + 'year' + ',' + bbb4 + ',' + 'end year' + ','
    #print(bbb2)
    ccc = ccc + bbb4
    #print(bbb4)
    #dict_of_songs.setdefault(year, []).append(songs)
    '''

#print(list_of_songs_for_year)
print(list_of_songs_for_year)

# print(list_of_songs_for_year[0])
# print(list_of_songs_for_year[1][0])

# li = list(list_of_songs_for_year[1].split(','))
# print(li[0])
# print(li[1])


'''
for i in range (0, len(list_of_songs_for_year)):
    li = list_of_songs_for_year[i].replace('],[', ',')
    #li1 = li[i].split(',')
'''

# print(list_of_songs_for_year[0])

# print(list_of_songs_for_year[1])

# ggg = list_of_songs_for_year[1].replace('],[', ',')

# li = list(list_of_songs_for_year[1].split('],['))


# print(li)
# print(li[0])
# print(li[1])

# print(li1)
# print(li1[2])


'''
for i in range (0, len(li)):
    if li[i] == 'year':
        print(li[i-1])
        print(li[i+5])
'''

#print(list_of_songs_for_year)

# print(dict_of_songs['1955'][0])

'''

left_identifier_song = '["'
    right_identifier_song = '"]'
    sss1 = "{}(.*?){}".format(*map(re.escape, (left_identifier_song, right_identifier_song)))
    songs1 = re.findall(sss1, str(songs))
    
    
print(list_of_songs_for_year)
for i in range(0, len(list_of_songs_for_year)):
    aaa = str(list_of_songs_for_year[i])
    bbb = aaa.replace("['", "")
    ccc = bbb.replace("']", "")
    #print(ccc)
    dict_of_songs.setdefault(i, []).append(str(ccc))

print(dict_of_songs)
#dict_of_songs.setdefault(year, []).append(songs)

#print(list_of_songs_for_year)
'''

# dict_of_songs = {'1951': [['"Nat King Cole","Too Young","KaFtsqU2V6U"],["Tony Bennett","Because of You","i-4zvArJDGg"],["Les Paul and Mary Ford","How High the Moon","NkGf1GHAxhE"],["Rosemary Clooney","Come on a My House","mriXncI96lw"],["Mario Lanza","Be My Love","8o8SZng55T0"],["The Weavers","On Top of Old Smoky","6J5O_YlfFqk"],["Tony Bennett","Cold Cold Heart","uORPxmsBJoE"],["Perry Como","If","aPqhvhlhCcs"],["Mario Lanza","The Loveliest Night of the Year","0VeiwX5wVtw"],["Patti Page","Tennessee Waltz","_Ek3eCbfqp0"],["Frankie Laine","Jezebel","dHvn1VH7q0E"],["Tony Martin","I Get Ideas","KVrLs5W9uco"],["Les Paul and Mary Ford","Mockin\' Bird Hill","S9Hje2BTvAo"],["Patti Page","Mockin\' Bird Hill","U7zrMzVNYwo"],["Guy Mitchell and Mitch Miller","My Heart Cries for You","WPeK2hj02Xo"],["Eddy Howard","(It\'s No) Sin","iozmjMYwzuY"],["Vaughn Monroe","Sound Off","3owoYQazL9o"],["Dinah Shore","Sweet Violets","LtnLvrmyh3E"],["Les Paul and Mary Ford","The World Is Waiting for the Sunrise","7iGXP_UBog4"],["Guy Mitchell and Mitch Miller","My Truly Truly Fair","QgDAsWJMGcg"],["The Four Aces","(It\'s No) Sin","_YgdVXQSYn0"],["Debbie Reynolds and Carleton Carpenter","Aba Daba Honeymoon","VJHJAkhacGU"],["Frankie Laine","Rose Rose I Love You","xpEGTSed1lI"],["Del Wood","Down Yonder","idURSDVwIVE"],["Billy Eckstine","I Apologize","oFVFkVyQGNQ"],["Patti Page","Would I Love You (Love You Love You)","1mvktmQ6Dm0"],["Perry Como and The Fontane Sisters","You\'re Just in Love","lhSyFHTfsXU"],["Ames Brothers with The Les Brown Orchestra","Undecided","EFjvUbxYqfA"],["Phil Harris","The Thing","-1tKZ3flZZY"],["Les Baxter","Because of You","Smhs33RMSh4"']]}
# print(dict_of_songs)

# print(dict_of_songs["1951"])

# result = re.findall('{}(.*){}'.format(left_identifier, right_identifier), s)
# print(result.group(1))

'''
vgm_url = 'http://thenostalgiamachine.com/y/#2009'
html_text = requests.get(vgm_url).text
print(html_text)
'''

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
