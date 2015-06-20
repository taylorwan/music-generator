# all the imports
from flask import Flask

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def show_index():
    return redirect_url('.onsets/'+songname)

@app.route('/onsets/<songname>',methods=['GET'])
def show_index():
    return 'hello world'

if __name__ == '__main__':
    app.run()
