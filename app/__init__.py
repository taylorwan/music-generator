# all the imports
from flask import Flask, request
import rhythmstring
import json

app = Flask(__name__)

@app.route('/onsets', methods=['GET'])
def play_song():
	song = request.args.get('song')
	artist = request.args.get('artist')
	onsets = rhythmstring.getOnsets(artist,song)
	return json.dumps(onsets)

if __name__ == '__main__':
    app.run()
