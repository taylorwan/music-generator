# all the imports
from flask import Flask

app = Flask(__name__)

@app.route('/onsets/<songname>/<artist>', methods=['GET'])
def play_song(songname, artist):
    return ('%s, %s' % (songname,artist))

if __name__ == '__main__':
    app.run()
