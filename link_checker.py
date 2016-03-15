import requests
import re
from selenium import webdriver
from MashupMap import db
from MashupMap.models import Mashup
from MashupMap.analytics import get_broken_index, save_broken_index

#need to update pip requirements

def check_youtube(url_check):
    r = requests.get(url_check) #requests url_check
    html = r.text #gets page source code (html)
    # print(str(html))
    match = re.search('Sorry about that', html) #searches for an error pattern from youtube using regex
    if match:
        return True
    else:
        return False

def check_soundcloud(url_check):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.get(url_check)
    html = driver.page_source
    #afterwards, I'll make it more efficient by using phantomJS to search instead of regex in the whole page source.
    match = re.search('We can.t find that track', html) #searches for error pattern form souncloud in source code
    #We can’t find that track.
    if match:
        return True
    else:
        return False


def check_vimeo(url):
    r = requests.get(url) #requests url_check
    html = r.text #gets page source code (html)
    # print(str(html))
    match = re.search('Sorry, there is no video here.', html) #searches for an error pattern from youtube using regex
    if match:
        return True
    else:
        return False


def check_link(url):
    if re.search('youtube', url):
        # print('youtube')
        return check_youtube(url)
    elif re.search('soundcloud', url):
        # print('soundcloud')
        return check_soundcloud(url)
    elif re.search('vimeo', url):
        return check_vimeo(url)
    else:
        return False
# print(check_youtube('https://www.youtube.com/watch?v=78dcPS9xRcc'))
# print(check_soundcloud('https://soundcloud.com/tesher/shake-it-off'))


def main():
    start_index = int(get_broken_index())
    print('Start index: ' + str(start_index))
    mashups = Mashup.query.filter(Mashup.id > str(start_index))
    # print('Mashups', mashups, '\n')
    try:
        for m in list(mashups):
            # print(m.url)
            print(m.id)
            if check_link(m.url) :
                print('Broken link!')
                m.isBroken = True
            else:
                m.isBroken = False

            if m.id % 30 == 0:
                db.session.commit()
                save_broken_index(m.id)
                print('Committing...')
    except Exception as e:
        print(e, e.args)
        db.session.commit()
        save_broken_index(m.id - 1)
        print('User interruption. Committing...')
        return

    db.session.commit()
    save_broken_index(m.id)
    print('Committed!')




if __name__ == '__main__':
    main()
