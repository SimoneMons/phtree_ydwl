import urllib.request


def validate_link(url):
    # url = 'https://www.youtube.com/watch?v=RB-RcX5DS5A&list=RDRB-RcX5DS5A&start_radio=1&t=7'
    html = urllib.request.urlopen(url)
    # print(html.read().decode())
    s = html.read().decode()
    s = s.replace('\n', '')

    video_not_available = s.find('"playabilityStatus":{"status":"ERROR"')
    private_video = s.find('"playabilityStatus":{"status":"LOGIN_REQUIRED"')

    print('Not available', video_not_available)
    print('Private', private_video)

    if video_not_available > 0 or private_video > 0:
        # Video not available
        return 1
    else:
        # Video available
        return 0

#validate_link('https://www.youtube.com/watch?v=L7j1fUAA-tg')
