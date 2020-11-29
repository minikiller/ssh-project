# f = open("../templates/demofile.txt", "r")
# print(f.read())

# import jinja
# dic = {"key1": "hello", "key2": "world"}
# jinja.renderfile("demofile.txt", dic, "targ.txt")

from collections import defaultdict
# dd = defaultdict(list)

with open("./configs/esn.csv") as f:
    my_list = list(f)
dict = defaultdict(list)
# data = content.split(",")
# print(data[0:])
# dict[data[0]]=data[0:]
for list in my_list:
    data = list.split(",")
    dict[data[0]] = data[1:]
    # print(data[1])
print(len(dict['sdsd']))
