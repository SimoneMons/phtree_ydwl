import urllib.request
import urllib.parse
import re


def search_songs_nm(year_to_downlad):
    # Nostalgia Machine page list of songs
    html = urllib.request.urlopen("http://thenostalgiamachine.com/js/years.min.js")
    s = html.read().decode()
    s = s.replace('\n', '')

    dict_of_songs = {}  # {'year': '', 'singer': '', 'title': '', 'link': ''}}
    list_of_years = []
    list_of_songs_for_year = []
    list_of_link_to_download = []

    # years of the songs
    years = re.findall(r'\_(\d{4})\={songs', s)
    for year in years:
        list_of_years.append(year)

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
        # print(year)
        for i in range(0, len(songs_string_1)):
            songs_string_2 = songs_string_1[i].split(',')
            # print(songs_string_2[1])
            dict_of_songs['year'] = year
            dict_of_songs['singer'] = songs_string_2[0].replace('[', '')
            dict_of_songs['title'] = songs_string_2[1]
            dict_of_songs['link'] = songs_string_2[2]
            list_of_songs_for_year.append(dict_of_songs.copy())

    for i in range(0, len(list_of_songs_for_year)):
        if list_of_songs_for_year[0]['year'] == year_to_downlad:
            list_of_link_to_download.append('https://www.youtube.com/watch?v=' +
                                            str(list_of_songs_for_year[i]['link']).replace('"', ''))

    return list_of_link_to_download


search_songs_nm('1951')
