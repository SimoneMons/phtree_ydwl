
import re

txt = "I like bananas & mandarinas"

x = txt.replace("&", "_")

x = x.replace(" ", "_")

print(x)
