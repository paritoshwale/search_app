from django.shortcuts import render
from app import app
from flask import render_template, request, jsonify
import requests
import sys
import forms
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()
users = {
    "hello": generate_password_hash("world"),
    "good": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/', methods=['POST'])
@auth.login_required
def main():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        #print('Submitted search word', form.title.data)
        API_KEY = "AIzaSyA9v2HELWPhnLsAs97dbWim-XrAfmwubAA"
        SEARCH_ENGINE_ID = "775ec41f0a04df663"
        page = 1
        links= []
        titles = []
        snippets= []
        count= [i for i in range(1,11)]
        count= [str(x) for x in count]
        start = (page - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={form.title.data}&start={start}"
        data = requests.get(url).json()
        #print(len(data))

        search_items = data.get("items")
        #print(len(search_items))
        x=0
        for i, search_item in enumerate(search_items, start=1):
            
            try:
                long_description = search_item["pagemap"]["metatags"][0]["og:description"]
            except KeyError:
                long_description = "N/A"
        
            title_ = search_item.get("title")
            titles.append(title_)

            snippet = search_item.get("snippet")
            snippets.append(snippet)

            html_snippet = search_item.get("htmlSnippet")

            link = search_item.get("link")
            links.append(link)

            summary =['|'.join(x) for x in zip(count, titles, snippets, links)]
            # overall =[x+'-'+y for x in titles for y in links]
        return render_template('main.html', form=form, title=summary)
    return render_template('main.html', form=form)

@app.route('/look-for', methods=["POST"])
@auth.login_required

def get_response():
    if request.method=='POST':
        API_KEY = "AIzaSyA9v2HELWPhnLsAs97dbWim-XrAfmwubAA"
        SEARCH_ENGINE_ID = "775ec41f0a04df663"
        page = 1
        posted_data = request.get_json()
        data = posted_data['data']
        start = (page - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={data}&start={start}"
        result = requests.get(url).json()
        search_items = result.get("items")

        return result
    else:
        return jsonify(str("Choose correct method"))