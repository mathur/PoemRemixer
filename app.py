import os

from flask import Flask, url_for, redirect, request, render_template
from pymarkovchain import MarkovChain

PORT = int(os.environ.get('PORT', 5000))

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/poem', methods=['POST'])
def poem():
    story = str(request.form['story'].encode('ascii', 'ignore'))
    lines = int(request.form['lines'])

    if not story:
        return redirect(url_for('index'))

    mc = MarkovChain()
    mc.generateDatabase(story)

    result = []
    for line in range(0, lines):
        new_line = mc.generateString()
        if new_line not in result:
            result.append(new_line)

    return render_template('poem.html', result=result, story=story)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)