from MashupMap.models import Counters, get_or_create
from MashupMap import db


def count_stuff(key):
    if key == "playcount":
        mycnt = get_or_create(db.session, Counters, key=key)
        mycnt.value += 1
        db.session.commit()


def print_stuff(key):
    if key == "playcount":
        mycnt = get_or_create(db.session, Counters, key=key)
        print(key + " ", mycnt.value)
