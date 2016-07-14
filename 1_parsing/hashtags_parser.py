import json
from pprint import pprint
import pandas as pd


def get_tweets(filepath):
    """
    Gets the tweets into a list of json objects and returns the list.
    """

    f = open(filepath)

    tweets = []

    for line in f:

        tweets.append(json.loads(line))

    f.close()

    return tweets


def get_hastags(json_list):
    """
    Accepts a list of json dictionaries and returns a dictionary containing
    id/hashtag pairs.
    """

    hashtags = {}

    # for each tweet
    for tw in json_list:

        # if tweet is a retweet
        if 'retweeted_status' in tw.keys():

            # outer level id and ht

            # number of hashtags
            num_ht = len(tw['entities']['hashtags'])
            outer_id = tw['id']

            # if there are hastags
            if num_ht > 0:

                hts = []

                for i in range(num_ht):

                    hts.append(tw['entities']['hashtags'][i]['text'])

                hashtags[outer_id] = hts

            # now inner level id and ht

            # number of hashtags in retweeted_status part
            num_ht2 = len(tw['retweeted_status']['entities']['hashtags'])
            inner_id = tw['retweeted_status']['id']

            # if there are hashtags
            if num_ht2 > 0:

                hts = []

                for i in range(num_ht2):

                    hts.append(tw['retweeted_status']['entities']['hashtags'][i]['text'])

                hashtags[inner_id] = hts

        # if tweet is not a retweet
        else:

            # ensure we are only taking valid tweets since my data has
            # a few non-tweets of the form "{"limit":{"track":1,"timestamp_ms":"1443909730865"}}"
            if 'entities' in tw.keys():

                # number of hashtags
                num_ht = len(tw['entities']['hashtags'])
                tw_id = tw['id']

                # if there are hashtags
                if num_ht > 0:

                    hts = []

                    for i in range(num_ht):

                        hts.append(tw['entities']['hashtags'][i]['text'])

                    hashtags[tw_id] = hts

    # return the dictionary containing id, list of hashtags pairs
    return hashtags


def get_mentions(json_list):
    """
    Accepts a list of json dictionaries and extracts the id and mentions and
    puts them into a dictionary and then returns that dictionary.
    """

    mentions = {}

    # for each tweet
    for tw in json_list:

        # if tweet is a retweet
        if 'retweeted_status' in tw.keys():

            # outer info

            num_mnt = len(tw['entities']['user_mentions'])
            outer_id = tw['id']

            # if there are mentions
            if num_mnt > 0:

                mts = []

                for i in range(num_mnt):

                    mts.append(tw['entities']['user_mentions'][i]['id_str'])

                mentions[outer_id] = mts

            # inner info
            num_mnt2 = len(tw['retweeted_status']['entities']['user_mentions'])
            inner_id = tw['retweeted_status']['id']

            # if there are mentions
            if num_mnt2 > 0:

                mts = []

                for i in range(num_mnt2):

                    mts.append(tw['retweeted_status']['entities']['user_mentions'][i]['id_str'])

                mentions[inner_id] = mts


        # tweet is not a retweet
        else:

            # check that we have a valid tweet because my tweets file contains some that
            # look like "{"limit":{"track":1,"timestamp_ms":"1443909730865"}}"
            if 'entities' in tw.keys():

                num_mnt = len(tw['entities']['user_mentions'])
                tw_id = tw['id']

                # if there are mentions
                if num_mnt > 0:

                    mts = []

                    for i in range(num_mnt):

                        mts.append(tw['entities']['user_mentions'][i]['id_str'])

                    mentions[tw_id] = mts

    return mentions


def dict_to_lists(tw_dict):
    """
    Accepts a dictionary of key/list pairs and converts it to a
    list of lists.
    """

    info = []
    keys = tw_dict.keys()

    for key in keys:

        n = len(tw_dict[key])

        for i in range(n):

            l = [key, tw_dict[key][i]]
            info.append(l)

    return info


def csv_writer(list_of_lists, filepath):
    """
    Accepts a list of lists containing tweet info, imports it to a
    pandas data frame, and writes that to a .csv file.
    """

    data = pd.DataFrame(list_of_lists)
    data.to_csv(filepath, encoding='utf-8-sig', index=False, header=False)


def main():

    # where your tweets are
    filename = "/sftweets.json"

    # where you want the hashtags
    fl_ht = '/hashtags.csv'

    # where you want the mentions
    fl_mt = '/mentions.csv'

    # get a list of tweets
    tweets = get_tweets(filename)

    # get a list of hashtag and mention info
    hashtags = dict_to_lists(get_hastags(tweets))
    mentions = dict_to_lists(get_mentions(tweets))

    # write hashtag and mention info to csv files
    csv_writer(hashtags, fl_ht)
    csv_writer(mentions, fl_mt)


main()












