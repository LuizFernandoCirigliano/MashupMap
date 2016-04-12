import requests
import re
from selenium import webdriver
from MashupMap import db
from MashupMap.models import Mashup
from MashupMap.analytics import get_index, save_index

#need to update pip requirements

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
sc_re = re.compile('We can.t find that track')

def find_error_message(error_message, page_source):
    if error_message in page_source:
        return True
    else:
        return False

def check_youtube(url_check):
    r = requests.get(url_check) #requests url_check
    html = r.text #gets page source code (html)
    youtube_error = 'Sorry about that'

    return find_error_message(youtube_error, html)
    match = re.search(youtube_error, html) #searches for an error pattern from youtube using regex

    if match:
        return True
    else:
        return False

def check_soundcloud(url_check):
    driver.get(url_check)
    html = driver.page_source
    soundcloud_error = 'We can.t find that track'
    #afterwards, I'll make it more efficient by using phantomJS to search instead of regex in the whole page source.
    # return find_error_message(soundcloud_error, html)
    # match = re.search(soundcloud_error, html) #searches for error pattern form souncloud in source code
    match = sc_re.search(html)

    if match:
        return True
    else:
        return False


def check_vimeo(url):
    r = requests.get(url) #requests url_check
    html = r.text #gets page source code (html)
    vimeo_error = 'Sorry, there is no video here.'

    return find_error_message(vimeo_error, html)
    match = re.search(vimeo_error, html) #searches for an error pattern from youtube using regex
    if match:
        return True
    else:
        return False


def check_link(url):
    if 'youtube' in url:
        return check_youtube(url)
    elif 'soundcloud' in url:
        return check_soundcloud(url)
    elif 'vimeo' in url:
        return check_vimeo(url)
    else:
        print('Website not identified!', url)
        return False
# print(check_youtube('https://www.youtube.com/watch?v=78dcPS9xRcc'))
# print(check_soundcloud('https://soundcloud.com/tesher/shake-it-off'))


def main():
    start_index = int(get_index("strt_index"))
    print('Start index: ' + str(start_index))
    mashups = Mashup.query.filter(Mashup.id >= start_index).order_by(Mashup.id)
    # print('Mashups', mashups, '\n')
    try:
        for m in mashups:
            # print(m.id)
            if m.isBroken != True:
                if check_link(m.url) : #deal with error where there is no url
                    print(m.id, 'Broken link!')
                    m.isBroken = True
                else:
                    m.isBroken = False
    except Exception as e:
        print(e, e.args, type(e))
        print('Interruption.')
    except:
        print('User interruption.')
    else:
        print('Finished!')
    finally:
        db.session.commit()
        if m.id >= mashups[-1].id:
            save_index("strt_index", 0)
        else:
            save_index("strt_index", m.id - 1)
        print('Comitting...')







if __name__ == '__main__':
    main()
