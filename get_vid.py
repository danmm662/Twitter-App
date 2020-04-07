import tweepy
from operator import itemgetter


"""
Gets the URL for an mp4 from a tweet in the highest bitrate possible
Returns None if URL cannot be found
"""

def get_vid_url(tweet):

    try:

        #Getting the video information from the tweet
        variants = tweet.extended_entities["media"][0]["video_info"]["variants"]

        #Remove the mpegURL
        for i in range(len(variants)):
           v = variants[i]
           if v["content_type"] == "application/x-mpegURL":
               variants.remove(v)
               break      

        #Sort the list by bitrate
        variants = sorted(variants, key=itemgetter('bitrate'), reverse=True) 

        url = variants[0]['url']
    
    #Video URL can't be found
    except (KeyError, AttributeError) as e:
        print(e)
        url = None

    return url