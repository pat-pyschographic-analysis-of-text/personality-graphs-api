from ibm_watson import PersonalityInsightsV3
import pandas as pd
import tweepy
import json
import time
import os

TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY'] 
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET)
TWITTER_AUTH.set_access_token(TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

TWEET_COUNT = 50

def main(event, context):
     # WARNING: this is a very expensive step
     # API call and store data
     # Do not set the num_periods over 5, it will eat up the API
    num_periods = 5
    name = input
    df_a = pd.DataFrame()

    for i in range(num_periods):
        try:
            twitter_user = TWITTER.user_timeline(screen_name=name,
                                          count=TWEET_COUNT,
                                          tweet_mode='extended',
                                          max_id=twitter_user.max_id)

            favorites = TWITTER.favorites(name,count=TWEET_COUNT,
                                       max_id=favorites.max_id)

            def convert_status_to_pi_content_item(t,f):
                     return {
                         'content': t.full_text + f.text,
                         'contenttype': 'text/plain',
                         'created': int(time.mktime(t.created_at.timetuple())),
                         'id': str(t.id),
                         'language': t.lang
                     }

            pi_content_items_array = list(map(convert_status_to_pi_content_item, twitter_user,
                                           favorites))

            pi_content_items = {'contentItems': pi_content_items_array}

            data = json.dumps(pi_content_items, indent=2)

            personality_insights = PersonalityInsightsV3(
             version='2017-10-13',
             url=pi_url,
             iam_apikey= pi_password)

            profile = personality_insights.profile(
                   data,
                   accept='application/json',
                   content_type='application/json',
                   consumption_preferences=True,
                   raw_scores=True).get_result()

            p = pd.DataFrame(profile['personality'],columns=['category','name','raw_score'])
            n = pd.DataFrame(profile['needs'], columns=['category','name','raw_score'])
            v = pd.DataFrame(profile['values'], columns=['category','name','raw_score'])
            df = pd.concat([p,n,v],axis=0)
            df['time'] = twitter_user[0].created_at
            df_a = df_a.append(df)

        except:
            twitter_user = TWITTER.user_timeline(screen_name=name,count=TWEET_COUNT,tweet_mode='extended')
            favorites = TWITTER.favorites(screen_name=name,count=TWEET_COUNT)
            def convert_status_to_pi_content_item(t,f):
                 return {
                     'content': t.full_text + f.text,
                     'contenttype': 'text/plain',
                     'created': int(time.mktime(t.created_at.timetuple())),
                     'id': str(t.id),
                     'language': t.lang
                 }

            pi_content_items_array = list(map(convert_status_to_pi_content_item, twitter_user,
                                           favorites))

            pi_content_items = {'contentItems': pi_content_items_array}

            data = json.dumps(pi_content_items, indent=2)

            personality_insights = PersonalityInsightsV3(
             version='2017-10-13',
             url=pi_url,
             iam_apikey= pi_password)

            profile = personality_insights.profile(
                   data,
                   accept='application/json',
                   content_type='application/json',
                   consumption_preferences=True,
                   raw_scores=True).get_result()

            p = pd.DataFrame(profile['personality'],columns=['category','name','raw_score'])
            n = pd.DataFrame(profile['needs'], columns=['category','name','raw_score'])
            v = pd.DataFrame(profile['values'], columns=['category','name','raw_score'])
            df = pd.concat([p,n,v],axis=0)
            df['time'] = twitter_user[0].created_at
            df_a = df_a.append(df)


    # Return proper data as json for other callbacks
    return {
        'statusCode': 200,
        'body': df_a.to_json(date_format='iso', orient='split')       
    } 
