
import os
import re
import sys

# pycharm exe
ffmpeg_path = ".\\ffmpeg\\ffmpeg.exe"
audio_path = os.path.expanduser('~\Downloads\_audio')

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        print(' ')
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("venv"), relative_path)


arr_webm = [x for x in os.listdir(audio_path) if x.endswith(".webm")]
print(arr_webm)

for file in arr_webm:
    filename_old = file
    filename_new = re.sub(r"\s+", '_', filename_old)
    os.rename(audio_path + '\\' + filename_old, audio_path + '\\' + filename_new)
    os.system(ffmpeg_path + ' -i ' + audio_path + '\\' + filename_new +
                                  ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')
    os.remove(audio_path + '\\' + filename_new)


#ffmpeg -i input.mp3 output.wma