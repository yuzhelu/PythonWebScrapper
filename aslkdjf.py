# testing stuff
from User import User
def check(name, array):
    for user in array:
        if user.name == name:
            return False
    return True
ar = []
if len(ar) == 0:
    print("zero")

name = "vt"
p = "abc"
user = User(name, p)
ar.append(user)
for user in ar:
    if user.name == name:
        print("==")

valid = check(name, ar)
print(valid)