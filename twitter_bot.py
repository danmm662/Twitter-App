import tweepy, time, _thread

import keys, get_vid


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

    seen_tweets = set()

    while True:

        try:
            for tweet in tweepy.Cursor(api.search, q="@DirectLinkBot download", result_type="recent", tweet_mode="extended").items(10):                

                #Make sure it is not a tweet we have already seen
                if tweet.id not in seen_tweets:

                    video_tweet_id = tweet.in_reply_to_status_id

                    #Ignore if the tweet isn't a reply
                    if video_tweet_id is not None:

                        video_tweet = api.get_status(video_tweet_id)
                        vid_url = get_vid.get_vid_url(video_tweet)

                        #If video URL can't be found
                        if vid_url is not None:

                            message = "Here's a direct link to the video you: " + vid_url + ". To download it, simply right click on it and press save as."                      
                            api.send_direct_message(tweet.user.id, message)

                            seen_tweets.add(tweet.id)
                        
                        else:
                            print("Video can't be found ")

                    else:
                        print("Not replying to any tweet")
                
                else:
                    print("Tweet already seen")


            time.sleep(60)

        except tweepy.TweepError as e:    

            #If we are rate limited by twitter, wait 15 minutes before trying again    
            if(e == tweepy.RateLimitError):
                print("Rate limited, timeout for a moment")
                time.sleep(900)                            
            
            else:
                print(e.reason)
                time.sleep(1)
        

main()