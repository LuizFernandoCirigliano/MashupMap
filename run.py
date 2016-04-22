from MashupMap import app
from config import PRODUCTION

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=(PRODUCTION==False))
