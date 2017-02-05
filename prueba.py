import tweepy

     
def main2():

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
        # # Mostramos los campos del objeto Tweet


        for tweet in tweets:
                #print "*********************************************"
                #print tweet.text.encode('utf-8')
                #print "------"  
                #print tweet.author.name
                #print "*********************************************"

                # Mostramos los campos del objeto Tweet
				#print tweet.author.name
				print "*********************************************"
				print "*********************************************"
				# Mostramos los campos del objeto author del Tweet
				#print tweet.author.followers_count
				print "*********************************************"
				print "*********************************************"
				# Mostramos el nombre del Autor del Tweet.
				#print tweet.author.followers_count
				#print tweet.author.statuses_count
				print("'" + tweet.author.name.encode('utf-8') + "'")







def main1():

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
                data += "<h2>" + tweet.author.name.encode('utf-8') + "</h2>" +  "<p>" + tweet.text.encode('utf-8') + "</p>"

        return data

def main():

    main2()


main()