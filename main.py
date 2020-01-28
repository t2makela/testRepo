#!/usr/bin/env python

from flask import Flask, escape, request, render_template_string
import urllib.request, json 


app = Flask(__name__)

template = "<html><head><title>{{ title }}</title></head><body><h1>{{ title }}</h1>{{ body|safe }}</body></html>"
form = """
<form action='/results' method='GET'>Business ID: <input type='text' name='id' />
<input type='submit' value='Submit'/></form>
"""
businessinfo = """
<p>Business ID: {{ id }}</p>
<p>Business name: {{ name }}</p>
<p>Address: {{ address }}</p>
<p>Industry: {{ industry }}</p>
<p>Company type: {{ type }}</p>
<p>Registration date: {{ regdate }} </p>
"""

# Index that displays form
@app.route('/')
def index():
    return render_template_string(template, title="Home", body=form)

# Display results
@app.route('/results', methods=['GET'])
def result():
    businessid = request.args.get('id')
    with urllib.request.urlopen("https://avoindata.prh.fi/bis/v1/" + businessid) as url:
        data = json.loads(url.read().decode())
        return render_template_string(template, title="Business information about: " + data['results'][0]['name'], body=render_template_string(businessinfo, 
        id = businessid, type = data['results'][0]['companyForms'][2]['name'], 
        industry = data['results'][0]['businessLines'][0]['name'], 
        address = data['results'][0]['addresses'][0]['street'] + ', ' + data['results'][0]['addresses'][0]['city'],
        name = data['results'][0]['name'], regdate = data['results'][0]['registrationDate']))

if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)