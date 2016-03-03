from config import basedir
import os


play_counter_path = os.path.join(basedir, 'playcounter.db')


def count_stuff(key):
    if key == "playcounter":
        try:
            with open(play_counter_path) as f:
                counter = int(f.read()) + 1
        except IOError:
            counter = 1
        with open(play_counter_path, "w") as f:
            f.write(str(counter))


def print_stuff(key):
    if key == "playcounter":
        with open(play_counter_path) as f:
            counter = int(f.read())
            print(counter)
