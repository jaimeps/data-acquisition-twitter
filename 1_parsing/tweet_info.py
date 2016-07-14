
import json
from pprint import pprint
import csv
import pandas as pd
import codecs
import re

FILE = 'pa10am.json'
FILECSV = 'TWEETS.csv'


def parse_json(json_file):
    with open(json_file) as data_file:
        data = []
        for line in data_file:
            data.append(json.loads(line))
    return data

def process(input):
    # return unicode(str(input).strip(codecs.BOM_UTF8),'utf-8').replace('\n', '')
    output = input.encode('utf-8', 'ignore').replace('\n',' ')
    output = re.sub(r'\W+', ' ', output)
    return output


def get_tweet_data(data, tweet_info_list, user_info_list, retweet_info_list):
    # input: data from json file; info: the information wanted in the user information of a tweet
    # output: a list of lists with each tweet info
    tweet_info = []
    for i in range(len(data)):
        tweet = []
        if 'id' in data[i].keys():
            # Obtain data at tweet level']
            for word in tweet_info_list:
                tweet.append(data[i][word])
            tweet.append(process(data[i]['text']))
            # Coordinates is at sublevel
            if data[i]['coordinates'] != None:
                tweet.append(data[i]['coordinates']['coordinates'])
            else:
                tweet.append(data[i]['coordinates'])
            # Then obtain data at user level
            for word in user_info_list:
                    tweet.append(data[i]['user'][word])
            # Then obtain data at retweet level if exists (otherwise set 'null')
            for word in retweet_info_list:
                if 'retweeted_status' in data[i].keys():
                    tweet.append(data[i]['retweeted_status'][word])
                else:
                    tweet.append('Null')
            tweet_info.append(tweet)
    return tweet_info

def write_data(tweet_info):
    # write data into a csv file
    data = pd.DataFrame(tweet_info)
    data.to_csv(FILECSV, mode='a', encoding='utf-8-sig', index=False, header=False)

def main():
    data = parse_json(FILE) # please change the name to your json file

    # part of the information we want
    tweet_info_list = ['id', 'created_at']
    user_info_list = ['id']
    retweet_info_list = ['id']

    tweet_info = get_tweet_data(data, tweet_info_list, user_info_list, retweet_info_list)

    print 'number of tweets:', len(tweet_info)
    # print the user information in first tweet

    write_data(tweet_info)

    print type('wd') == str

if __name__ == "__main__":
    main()