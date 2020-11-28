# f = open("../templates/demofile.txt", "r")
# print(f.read())

import jinja

dic = {"key1": "hello", "key2": "world"}
jinja.renderfile("demofile.txt", dic, "targ.txt")
