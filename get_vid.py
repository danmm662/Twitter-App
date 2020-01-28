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
        variants.pop()

        #Sort the list by bitrate
        variants = sorted(variants, key=itemgetter('bitrate'), reverse=True) 

        url = variants[0]['url']
        
        #print(variants)
        #print(type(variants))
        #print(len(variants))
        #print(url)
    
    except (KeyError, AttributeError) as e:
        print("Video URL cannot be found")
        url = None

    return url