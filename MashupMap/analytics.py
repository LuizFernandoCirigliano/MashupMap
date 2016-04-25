from MashupMap.models import Counters
from MashupMap.helpers import get_or_create
from MashupMap import db

key_list = ["strt_index", "scr_index"]


def count_stuff(key):
    if key == "playcount":
        mycnt = get_or_create(db.session, Counters, key=key)
        mycnt.value += 1
        db.session.commit()


def print_stuff(key):
    if key == "playcount":
        mycnt = get_or_create(db.session, Counters, key=key)
        print(key + " ", mycnt.value)


def save_index(key, start_index):
    if key in key_list:
        mycnt = get_or_create(db.session, Counters, key=key)
        mycnt.value = start_index
        db.session.commit()

def get_index(key):
    if key in key_list:
        mycnt = get_or_create(db.session, Counters, key=key)
        return mycnt.value

def save_broken_index(start_index):
    key = "strt_index"
    mycnt = get_or_create(db.session, Counters, key=key)
    mycnt.value = start_index
    db.session.commit()


def get_broken_index():
    key = "strt_index"
    mycnt = get_or_create(db.session, Counters, key=key)
    return mycnt.value

def save_score_index(start_index):
    key = "scr_index"
    mycnt = get_or_create(db.session, Counters, key=key)
    mycnt.value = start_index
    db.session.commit()

def get_score_index():
    key = "scr_index"
    mycnt = get_or_create(db.session, Counters, key=key)
    return mycnt.value
