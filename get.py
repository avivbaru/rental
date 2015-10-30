import json
from rental import *

file_name = "./objects.json"


def get_offers(num=10):
    objects = get_objects()

    return sorted(objects, key=lambda obj: obj.submit_date)[:num]


def add_offer(offer):
    objects = get_objects()
    new_objects = [str(offer)] + objects
    write_objects(new_objects)
    

def write_objects(new_objects):
    print new_objects
    object_str = json.dumps({"objects": new_objects})
    print object_str
    with open(file_name, "w") as f:
        f.write(object_str)
        f.close()


def get_objects():
    with open(file_name) as f:
        str_objects = f.readline()
    objects = json.loads(str_objects)

    return objects["objects"]


a = Product("test", "a")

print get_offers()
add_offer(a)

a = Product("test2", "aa")

print get_offers()
add_offer(a)

print get_offers()