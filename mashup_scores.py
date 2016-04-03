import praw
import re
import os
from MashupMap import db
from MashupMap.models import Mashup
from MashupMap.analytics import *

KEY_LAST_REDDIT = 'last_reddit_mashup'

user_agent = os.environ.get('USER_AGENT', 'Default_User_Agent_For_Mashups')
r = praw.Reddit(user_agent=user_agent)

def get_mashup_id(url):
    match = re.search('comments/\w+', url)
    if not match:
        print('Mashup url couldnt be parsed.')
        return None
    # print(match)

    id = match.group(0)[len('comments/'):]
    return id

def update_score(mashup, submission_id):
    submission = r.get_submission(submission_id)
    score = submission.score
    mashup.score = score
    # db.session.commit()



def main():
    start_index = int(get_index("scr_index"))
    print('Start index: ' + str(start_index))
    mashups = Mashup.query.filter(Mashup.id > start_index).order_by(Mashup.id)
    # print("Length of mashups: {}".format(len(mashups)))
    try:
        for i,m in enumerate(mashups):
            print('Submission id: {}'.format(m.id))
            submission_id = get_mashup_id(m.permalink)
            try:
                submission = r.get_submission(submission_id=submission_id)
            except Exception as e:
                print(e)
            score = submission.score
            m.score = score
            print(m.score)
    except Exception as e:
        print(e, e.args)
        print('Interruption.')
    except:
        print('User interruption.')
    else:
        print('Finished!')
    finally:
        db.session.commit()
        save_index("scr_index", m.id - 1)
        print('Comitting...')





if __name__ == '__main__':
    main()
