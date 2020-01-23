import tweepy, time, _thread

import keys


auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

#Helper method to delete tweets
def deleteThread(api, objectId):
	try:
		api.destroy_status(objectId)
		print('Deleted a tweet')
	except:
		print("Failed to delete")

#Removes all tweets and retweets 
def delete_all_tweets():
    for status in tweepy.Cursor(api.user_timeline).items():
       try:
           #api.destroy_status(status.id)
           #print "Deleted:", status.id
           _thread.start_new_thread( deleteThread, (api, status.id, ) )
       except:
           print("Failed to delete: " + str(status.id))

def main():

    replied_tweets = set()

    while True:

        try:
            for tweet in tweepy.Cursor(api.search, q="@test_tastie hello mate").items(5):    
                
                if tweet.id not in replied_tweets:
                
                    try:  
                        tweetId = tweet.user.id
                        username = tweet.user.screen_name
                        api.update_status("@" + username + " hello brother, how you going?", in_reply_to_status_id = tweet.id_str)
                        print('Replied to tweet')
                        replied_tweets.add(tweet.id)
                    except tweepy.TweepError as e:        
                        print(e.reason)
                
                else:
                    print("Tweet already replied to")


                time.sleep(60)

        except tweepy.TweepError as e:        
            print(e.reason)
            time.sleep(1)
        

main()