# -*- coding: utf-8 -*-
# Mongodb -> http://funnyfrontend.com/instalar-mongodb-y-uso-de-comandos-basicos/

from flask import Flask, render_template, request, session, jsonify
from pymongo import MongoClient
import tweepy , feedparser
import os
from flask_googlemaps import GoogleMaps

app = Flask(__name__)
app.secret_key = 'super secret key'

counter = 0

# you can also pass the key here if you prefer
GoogleMaps(app, key="AIzaSyBd-UKqks6mhY9MAgeY-XhOKr9-z8HmENc")

# Abrir la base  de datos de usuarios
def init_db():

	# Creamos un cliente para ejecutar una instancia de mongodb
	client = MongoClient()

	# Abrimos la base de datos usuarios
	db = client['users']

	return db

@app.route("/")
def start():

	if 'uname' in session:
		session['urls'].append('index')

		if len(session['urls']) > 3:
			session['urls'].pop(0)

	return render_template('index.html')

@app.route("/index")
def get_index():

	if 'uname' in session:
		#session['urls'].append('index')
		session['urls'] = session['urls']+['index'] 

		if len(session['urls']) > 3:
			session['urls'].pop(0)

	return render_template('index.html')		

@app.route("/about")
def get_about():

	if 'uname' in session:
		#session['urls'].append('about')
		session['urls'] = session['urls']+['about'] 

		if len(session['urls']) > 3:
			session['urls'].pop(0)

	markers = get_markers()	

	return render_template('about.html', markers = markers)

@app.route("/graphics")
def get_graphics():

	if 'uname' in session:
		#session['urls'].append('gallery')
		session['urls'] = session['urls'] + ['gallery'] 

		if len(session['urls']) > 3:
			session['urls'].pop(0)

	names ,values = get_dataGraphics()	
	n = len(values)


	names2, followers, statuses, n2 = get_dataTweets()


	names[0] = 'Mixed'
	names[6] = 'Latin'

	return render_template('graphics.html', names = names, values = values, n = n,
							names2 = names2, followers = followers, statuses = statuses, n2 = n2+1)


@app.route("/user")
def get_user():
	
	if 'uname' in session:
		
		db = init_db()
		user = db.member.find_one({"Username": session['uname']})	

		session['urls'] = session['urls']+['user'] 

		if len(session['urls']) > 3:
			session['urls'].pop(0)
	
		return render_template('user.html',user = user)

	return render_template('index.html')	

@app.route("/tweets")
def get_tweets_page():

	if 'uname' in session:
		#session['urls'].append('about')
		session['urls'] = session['urls']+['tweets'] 

		if len(session['urls']) > 3:
			session['urls'].pop(0)

	return render_template('tweets.html')

@app.route("/rss")
def get_rss():

	if 'uname' in session:
		#session['urls'].append('about')
		session['urls'] = session['urls']+['rss'] 

		if len(session['urls']) > 3:
			session['urls'].pop(0)

	feed = feedparser.parse('http://ep00.epimg.net/rss/elpais/ciencia.xml',25)

	news = feed['items']


	return render_template('rss.html', news = news)


#****************************** P4: GESTIÓN DE USUARIOS *************************************

@app.route('/login', methods=['GET', 'POST'])
def login():	

	db = init_db()

	if request.method == 'POST':
		uname = request.form['uname']
		psw = request.form['psw'] 
		user = db.member.find_one({"Username": uname, "Password": psw})

		if user != None :			 
			session['uname'] = uname
			session['urls'] = []

			return render_template('user.html', user = user)
		
	return render_template('index.html')

@app.route('/change',methods=['GET', 'POST'])
def change():

	db = init_db()

	if request.method == 'POST':

		db.member.update(
   			{ "Username":  session['uname'] },
   			{
      			'Username' : request.form['nombre'],
      			'Password':request.form['cont'],
      			'Email' : request.form['email'], 
   			},
		)

		user = db.member.find_one({"Username": request.form['nombre']})	

	return render_template('user.html',user = user)

@app.route('/logout')
def logout():

    # remove the username from the session if it's there
	session.pop('uname', None)

	return render_template('index.html')

@app.route('/modificar')
def modify():
	return render_template('datos.html')

#****************************** P5: PAGINADOR *************************************#

@app.route("/restaurantes")
def get_restaurantes():

	if 'uname' in session:
		#session['urls'].append('about')
		session['urls'] = session['urls']+['restaurantes'] 

		if len(session['urls']) > 3:
			session['urls'].pop(0)

	data = get_dbResturants()

	return render_template('restaurantes.html', data = data)


@app.route('/get_db_Rest')
def get_dbResturants():

	# Creamos un cliente para ejecutar una instancia de mongodb
	client = MongoClient()
	# Abrimos la base de datos de restaurantes
	db = client['test']
	global counter

	restaurants = db.restaurants.find().skip(counter).limit(10)
	data = ""

	for restaurant in restaurants:
		data += "<h2>" + restaurant['name'] + "</h2>" +  "<p>" + restaurant['borough'] + " , " +  restaurant['cuisine']   + "</p>"
	return data

@app.route('/get_nextRest')
def get_NextResturants():

	global counter
	counter += 10

	data = get_dbResturants()

	return data


#****************************** P6: RRSS, RSS , Maps, Gráficas *************************************#

@app.route('/get_dataGraphics')
def get_dataGraphics():

	# Creamos un cliente para ejecutar una instancia de mongodb
	client = MongoClient()

	# Abrimos la base de datos de restaurantes
	db = client['test']

	restaurants = db.restaurants.find().limit(100)

	names = []
	quantity = []
	dic = {}

	for restaurant in restaurants:
		try:
			dic[restaurant['cuisine']] += 1
		except:
			dic[restaurant['cuisine']] = 1

	for key in dic:
		names.append(key)
		quantity.append(dic[key])

	return names,quantity


@app.route('/get_dataTweets')
def get_dataTweets():

	# Consumer keys and access tokens, used for OAuth
	consumer_key = "0HkiLZyFdyV4SQU6CC937pOhM"
	consumer_secret = "8wXUEsLsxKsNQEWOfpeYZuod77g7xaxVKAnyP96k1p80SfrbT6"
	access_token = "808814353382305792-fExrmP8kbkZTHVQxhgLbs7OJun7m9VD"
	access_token_secret = "y1r2kPBlxWS0dwu6NAgTzC9x8wKJLOcvInsJhx9w4jtcJ"

	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)

	# https://dev.twitter.com/docs/api/1.1/get/search/tweets
	tweets = api.search(q="ibiza", count=5)

	names = []
	followers = []
	statuses = []

	for tweet in tweets:
		try:
			names.append(tweet.author.name.encode('ascii').strip())
		except:
			names.append('User')
		followers.append(tweet.author.followers_count)
		statuses.append(tweet.author.statuses_count)

	n = len(names)

	return names,followers,statuses,n




@app.route('/get_tweets')
def get_tweets():

	# Consumer keys and access tokens, used for OAuth
	consumer_key = "0HkiLZyFdyV4SQU6CC937pOhM"
	consumer_secret = "8wXUEsLsxKsNQEWOfpeYZuod77g7xaxVKAnyP96k1p80SfrbT6"
	access_token = "808814353382305792-fExrmP8kbkZTHVQxhgLbs7OJun7m9VD"
	access_token_secret = "y1r2kPBlxWS0dwu6NAgTzC9x8wKJLOcvInsJhx9w4jtcJ"

	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)

	# https://dev.twitter.com/docs/api/1.1/get/search/tweets
	tweets = api.search(q="ibiza", count=5)

	data = ""

	for tweet in tweets:
		#for tweet in tweets:
		data += "<h4>" + tweet.author.name.encode('utf-8') + "</h4>" +  "<p>" + tweet.text.encode('utf-8') + "</p>"

	return data

@app.route("/get_markers")
def get_markers():

	# Creamos un cliente para ejecutar una instancia de mongodb
	client = MongoClient()

	# Abrimos la base de datos de restaurantes
	db = client['test']

	markers = []

	restaurants = db.restaurants.find().limit(100)

	for restaurant in restaurants:
		aux = (restaurant['address']['coord'][1], restaurant['address']['coord'][0])
		markers.append(aux)

	return markers

#****************************** 404 *************************************#
@app.errorhandler(404)
def page_not_found(error):
    return "Página no encontradaaa", 404

if __name__ == "__main__":
	# Para que Flask ponga la aplicacion disponible en todos los interfaces
	
    app.debug = False
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
