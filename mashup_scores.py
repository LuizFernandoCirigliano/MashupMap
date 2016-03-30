import praw
import re
import os
from MashupMap import db
from MashupMap.models import Mashup

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

def update_score(submission_id):
    submission = r.get_submission(submission_id)

def main():
    # m_id = get_mashup_id('https://www.reddit.com/r/mashups/comments/4ckylm/totom_adele_loves_someone_like_kanye_k_west_adele/')
    m_id = get_mashup_id('https://www.reddit.com/r/explainlikeimfive/comments/4clbhm/eli5_what_do_all_of_these_leaked_emails_from_big/')
    print(m_id)



if __name__ == '__main__':
    main()
