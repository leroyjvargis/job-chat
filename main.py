import datetime

from flask import Flask, jsonify, request, abort
import engine

app = Flask(__name__)


@app.route('/')
def root():
    message = "All your base are belong to us!"
    return jsonify({'message': message})

@app.route('/search', methods=['POST'])
def search():
    if not request or not request.json:
        abort(400)
    searchQuery = request.json
    results = engine.getResults(searchQuery)
    return jsonify(results)

@app.route('/addJob', methods=['POST'])
def add():
    if not request or not request.json:
        abort(400)
    engine.addRecord(request.json)
    return jsonify(success=True)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
