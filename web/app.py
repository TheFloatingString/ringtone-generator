from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # generate the ringtone and save it to static folder
        midi_filename = 'tune2.m4a'
        return render_template('main.html', ringtone=midi_filename)
    else:
        return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
