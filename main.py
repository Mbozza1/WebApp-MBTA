from flask import Flask, render_template, request, redirect, url_for
import mbta_helper
import json
import urllib.request
from urllib.parse import urlencode

# Create a flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Index page
# @app.route('/')
# def hello():
#   return render_template('index.html')
 # Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        place = request.form['place']
        transportation_type = request.form['transportation_type']
        stop_info = mbta_helper.find_stop_near(place,transportation_type)
        if stop_info:
            return render_template('mbta_station.html', stop_info=stop_info)
        else:
            return render_template('error.html')
    return render_template('index.html')

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0', debug=True, port=8080)
