import tweepy, time, _thread
import keys, get_vid

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

        #Ignore retweets
        if not hasattr(status, "retweeted_staus"):
            #Check that tweet is in reply to another tweet
            video_tweet_id = status.in_reply_to_status_id

             #Ignore if the tweet isn't a reply
            if video_tweet_id is not None:

                video_tweet = api.get_status(video_tweet_id)
                vid_url = get_vid.get_vid_url(video_tweet)

                #Video found, send link to user
                if vid_url is not None:
                    message = "@" + status.user.screen_name + " Here's a direct link to the video: " + vid_url + ". To download it, simply right click on the video and press save as."                      
                    api.update_status(message, in_reply_to_status_id = status.id) #send_direct_message(tweet.user.id, message)
                
                #Video cannot be found, let user know
                else:
                    message = "@" + status.user.screen_name + " Video cannot be found sorry."
                    api.update_status(message, in_reply_to_status_id = status.id)


    def on_error(self, status_code):
        print("Encountered streaming error:", status_code)
        time.sleep(900)


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

if __name__ == "__main__":

    auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
    auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

    tags = ["@VideoLinkBot"]
    myStream.filter(track=tags)