
import json
from pprint import pprint
import csv
import pandas as pd

def parse_json(json_file):
    with open(json_file) as data_file:
        data = []
        for line in data_file:
            data.append(json.loads(line))
    return data

def get_user_data(data, user_info_list):
    # input: data from json file; info: the information wanted in the user information of a tweet
    # output: a list of lists with the user's info
    user_info = []
    for i in range(len(data)):
        user = []
        if 'id' and 'user' in data[i].keys():
            for word in user_info_list:
                user.append(data[i]['user'][word])
            user_info.append(user)
        re_user = []
        if 'retweeted_status' in data[i].keys():
            for word in user_info_list:
                re_user.append(data[i]['retweeted_status']['user'][word])
            user_info.append(re_user)
    return user_info

def write_data(tweet_user_info):
    data = pd.DataFrame(tweet_user_info)
    data.to_csv('user_pa10v2.csv', encoding='utf-8-sig', index=False, header=False)

def main():
    data = parse_json('twitter_output.json') # please change the name to your json file

    # part of the information we want
    user_info_list = ['id', 'name', 'followers_count', 'following', 'friends_count', 'profile_background_color', 'statuses_count',
                      'location']

    tweet_user_info = get_user_data(data, user_info_list)

    print 'number of tweets:', len(tweet_user_info)
    # print the user information in first tweet

    write_data(tweet_user_info)

    print type('wd') == str

if __name__ == "__main__":
    main()