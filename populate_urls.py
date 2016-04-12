from MashupMap import db
from MashupMap.models import Mashup
from urllib import parse


def get_url_from_embed(embed_code):
    try:
        url_start = embed_code.index("url=") + 4
        url_end = embed_code.index("&", url_start)
        url = embed_code[url_start:url_end]
        url = parse.unquote(url)
        return url
    except ValueError:
        try:
            url_start = embed_code.index("src=\"") + 5
            url_end = embed_code.index("\"", url_start)
            url = embed_code[url_start:url_end]
            url = parse.unquote(url)
            return url
        except:
            return None


def main():
    mashups = Mashup.query.all()
    for m in mashups:
        m.url = get_url_from_embed(m.content)
    db.session.commit()

    mashups_check = Mashup.query.all()
    print([m.url for m in mashups_check])

if __name__ == '__main__':
    main()
