import io
import os
import json

import responder
from wordcloud import WordCloud


env = os.environ
DEBUG = env['DEBUG'] in ['1', 'True', 'true']
FORMAT = env['FORMAT']
FONT_FILE_NAME = env['FONT_FILE_NAME']

cur_dir = os.path.dirname(__file__)
FONT_PATH = os.path.join(cur_dir, 'fonts', FONT_FILE_NAME)
with open(os.path.join(cur_dir, 'wordcloud.json')) as fp:
    CONFIG = json.load(fp)
CONFIG['font_path'] = FONT_PATH

api = responder.API(debug=DEBUG)
wordcloud = WordCloud(**CONFIG)


@api.route("/")
async def generate(req, resp):
    body = await req.text
    json_body = json.loads(body)

    if json_body.get('frequencies'):
        image = wordcloud.generate_from_frequencies(
            json_body['frequencies']
        ).to_image() 
    else:
        image = wordcloud.generate_from_text(
            json_body['text']
        ).to_image() 

    with io.BytesIO() as bytes_io:
        image.save(bytes_io, format=FORMAT)
        content = bytes_io.getvalue()

    resp.content = content


if __name__ == "__main__":
    api.run()