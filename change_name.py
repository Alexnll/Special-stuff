import os
import re
path = 'D:/picture/'
f = os.listdir(path)
n = 0
for i in f:
    old_name = path + f[n]
    if re.match('.*\.(\w{3})', f[n]).group(1) == "jpg":
        new_name = path + 'pic' + str(n+1) + '.jpg'
        os.rename(old_name, new_name)
        print(old_name, '======>', new_name)
    else:
        new_name = path + 'pic' + str(n+1) + '.png'
        os.rename(old_name, new_name)
        print(old_name, '======>', new_name)
    n += 1