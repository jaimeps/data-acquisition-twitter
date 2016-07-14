
import json
import pandas as pd

def parse_json(json_file):
    with open(json_file) as data_file:
        data = []
        for line in data_file:
            data.append(json.loads(line))
    return data

def get_retweet_data(data, tweet_info_list, user_info_list, retweet_info_list):
    # input: data from json file; info: the information wanted in the user information of a tweet
    # output: a list of lists with each tweet info
    retweet_info = []
    for i in range(len(data)):
        retweet = []
        if 'retweeted_status' not in data[i].keys():
            pass
        else:
            retweetdata = data[i]['retweeted_status']
            if 'id' in retweetdata.keys():
                # Obtain data at tweet level
                for word in tweet_info_list:
                    retweet.append(retweetdata[word])
                # Coordinates is at sublevel
                if retweetdata['coordinates'] != None:
                    retweet.append(retweetdata['coordinates']['coordinates'])
                else:
                    retweet.append(retweetdata['coordinates'])
                # Then obtain data at user level
                for word in user_info_list:
                        retweet.append(retweetdata['user'][word])
                # Then obtain data at retweet level if exists (otherwise set 'null')
                for word in retweet_info_list:
                    if 'retweeted_status' in retweetdata.keys():
                        retweet.append(retweetdata['retweeted_status'][word])
                    else:
                        retweet.append('Null')
                retweet_info.append(retweet)
    return retweet_info

def write_data(tweet_info):
    # write data into a csv file
    data = pd.DataFrame(tweet_info)
    data.to_csv('tweet_tabletest.csv', encoding='utf-8-sig', index=False, header=False)

def main():
    data = parse_json('datadump.json') # please change the name to your json file

    # part of the information we want
    tweet_info_list = ['id_str', 'created_at', 'text']
    user_info_list = ['id_str']
    retweet_info_list = ['id_str']

    tweet_info = get_retweet_data(data, tweet_info_list, user_info_list, retweet_info_list)

    print 'number of tweets:', len(tweet_info)
    # print the user information in first tweet

    write_data(tweet_info)

main()
