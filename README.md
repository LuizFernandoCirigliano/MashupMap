# Mashup Map

This is a visualization of the most recent mashups posted to reddit/r/mashups

An edge between two artists means that there is a mashup made of their songs, clicking an edge will display the song.


Installing:

- You must have on your computer: python 3, pip, virtualenv.
- Clone the repository.
- Copy the path of your python 3 interpreter.
- Execute: 'virtualenv venv -p [path_to_your_python_interpreter]'.
- Append to the file venv/bin/activate the following: 'export USER_AGENT="[bot_name_of_your_choice]" '
- Execute: 'source venv/bin/activate'
- Execute: 'pip install -r requirements.txt'
- Execute: 'python db_create.py'
- Execute: 'python reddit_downloader.py'
- To run the app: 'python run.py'

Hosted on Heroku:

http://stark-refuge-87328.herokuapp.com
