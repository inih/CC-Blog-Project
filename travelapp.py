from flask import Flask, redirect, render_template, jsonify, request, json, request, url_for
import csv, json
import requests
import requests_cache
from cassandra.cluster import Cluster

#As this app involves the use of a created API & external API service, cache is needed to ensure that we aren't fetching and waste API restrictions.
requests_cache.install_cache('travelapp', backend='sqlite', expire_after=36000)

#The below code opens a file which as information regarding an individual's travel and stores it in a variable.
with open('records2.json') as f:
    all_posts = json.load(f)

#This then writes it to a csv. The aim of this is to store the blog entries in a csv and save to the cloud database
#This will later be implemented.
x = all_posts[0]['BlogEntries']
f = csv.writer(open("test.csv", "w"))
f.writerow(["Passage", "Location", "Title"])
for x in x:
    f.writerow([x["Passage"],
                x["Location"],
                x["Title"]])

#The cluster object is created so that when connecting to the database, we can connect to any IP address within our Cassandra Service in GC
#If you want to run locally, comment out the 2 lines below
cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

#These are the base URL formats of the external APIs used in this app
#APIXU is for weather and PIXABAY is for images
weather_url_template = 'http://api.apixu.com/v1/current.json?key={API_KEY}&q={CITY}'
pixabay_url_template = 'https://pixabay.com/api/?key={API_KEY}&q={CITY}&lang=en&category=travel&safesearch=true&per_page=3'


#This is the home page of the app
@app.route('/')
@app.route('/index/')
def hello():
    return render_template('index.html', title='Home')

#The below requests for the location of the user from the home page.
@app.route('/result', methods=['POST'])
def location_request():
    result = request.form

    city = result.get('user_location')
    city = city.capitalize()
    #These next two lines retieve the API keys from the config files and is passed into the template URLs
    weather_url = weather_url_template.format(API_KEY=app.config['WEATHER_API_KEY'], CITY=city)
    pixabay_url = pixabay_url_template.format(API_KEY=app.config['PIXABAY_API_KEY'], CITY=city)
    #The next two lines request the services
    resp2 = requests.get(pixabay_url)
    resp = requests.get(weather_url)

    #If the responses are 'ok' then both data is loaded into a dictionary for easier handling.
    if (resp.ok and resp2.ok):
        resp_dict = json.loads(resp.text)

        updatedDictVariables = updateDictV(resp_dict)
        resp2_dict = json.loads(resp2.text)

        image = resp2_dict['hits'][0]['largeImageURL']
        temp2 = updatedDictVariables['current']
    #If there was an issue with the request, then it will respond with the reasoning.
    else:
        return("Unfortunately, the city you have entered has resulted in an error, please enter an appropriate city + The errors are: + Weather Status Code: {} + Weather Reason: {} + Images Status Code {} + Images Reason {} +").format(resp.status_code, resp.reason, resp2.status_code, resp2.reason)

    return render_template("result.html", pictures=image, location=city, result=temp2), 200

#Users also have the ability to create new blog entries. It must include the story, title and location.
@app.route('/newpost', methods=['POST'])
@app.route('/newpost/', methods=['POST'])
def createPost():
    if not request.json:
        return jsonify({'Error':'The new entry must have a title, location and passage (ofc ;)'}), 400
    new_entry = {
        'title': request.json['title'],
        'location': request.json['location'],
        'passage': request.json['passage']
    }
    #It appended to the 'all-post' variable and saved
    all_posts.append(new_entry)
    with open ('recordsOutput.json','w') as g:
        json.dump(all_posts, g)

    #Returns a sucess message.
    return jsonify({'message': 'created: /newpost/{}'.format(new_entry['title'])}), 201

#This retrieves all posts created in json format.
@app.route('/posts', methods=['GET'])
@app.route('/posts/', methods=['GET'])
def entries():
    return jsonify(all_posts)

#This depends on the request sent. The user can either get a post or delete. Delete can only be done through a terminal request
#Users can search for specific entries and will return it in json format.
#Error handling with the appropriate message if not correct or in the data
@app.route('/posts/<post_title>', methods=['GET', 'DELETE'])
def postDeleteOrGet(post_title):
    if request.method == 'GET':
        posts = [post for post in all_posts[0]['BlogEntries'] if post['Title'] == post_title]
        location_posts = [lPost for lPost in all_posts[0]['BlogEntries'] if lPost['Location'] == post_title]
        if(len(posts) == 0 and len(location_posts) == 0):
            return jsonify({'error':'Post entry not found!'}), 404
        elif (len(posts) > 0 and len(location_posts) == 0):
            response = posts
            return jsonify(response)
        elif (len(location_posts) > 0 and len(posts) == 0):
            response = location_posts
            return jsonify(response)
        else:
            return jsonify(location_posts)
    #Users can delete entries if the send a delete request to the app
    if request.method == 'DELETE':
        matching_post = [post for post in all_posts[0]['BlogEntries'] if post['Title'] == post_title]
        if len(matching_post) == 0:
            return ({'error':'Post entry not found!'}), 404
        all_posts[0]['BlogEntries'].remove(matching_post[0])
        return jsonify({'success':True}), 200

#This function is specifically for the database and won't work if the first 2 cassandra lines above are commented route
#This function searches for a post in the database if it matches the name the user enters.
#BAd for SQL injection
@app.route('/posts/db/<post_title>', methods=['GET'])
def showPost(post_title):
	response = '<h1>That entry does not exist!</h1>'
	rows = session.execute( """Select * From travelrecords.posts where Title = '{}'""".format(post_title))
	for entry in rows:
		response = ('<h1> {} </h1><br><h2>Location: {} </h2><br><h2>Post:</h2><br><p> {} </p>'.format(post_title, entry.location, entry.passage))
	return(response)

#As the app deals with external API we need to filter the specific fields that are neccessary for the app
def updateDictV(dict):
    dict['current']['Last Updated'] = dict['current']['last_updated']
    del dict['current']['last_updated']
    dict['current']['Celsius'] = dict['current']['feelslike_c']
    del dict['current']['feelslike_c']
    dict['current']['Temperature_C'] = dict['current']['temp_c']
    del dict['current']['temp_c']
    dict['current']['UV Value'] = dict['current']['uv']
    del dict['current']['uv']
    dict['current']['Wind_MPH'] = dict['current']['wind_mph']
    del dict['current']['wind_mph']
    dict['current']['Precipitation_IN'] = dict['current']['precip_in']
    del dict['current']['precip_in']
    dict['current']['Humidity'] = dict['current']['humidity']
    del dict['current']['humidity']
    dict['current']['Condition'] = dict['current']['condition']['text']
    del dict['current']['condition']
    return (dict)

#This allows the program to be exposed through port 8080
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
