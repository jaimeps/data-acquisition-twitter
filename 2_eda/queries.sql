
DROP SCHEMA tw CASCADE;
CREATE SCHEMA tw;

/* TABLE TWEETS */
CREATE TABLE tw.tweets (tweet_id char(20), created_time TIMESTAMP(30), message varchar(200),
  location char(30),user_id char(20), retweet_id char(20));
commit;
COPY tw.tweets from '/TWEETS.csv' WITH (FORMAT CSV, DELIMITER ',', ENCODING 'utf-8');
commit;

/* TABLE USER */
create table tw.user(
 id char(20),
 name char(30),
 followers_count FLOAT,
 following_count float,
 friends_count float,
 profile_background_color char(20),
 statuses_count FLOAT,
 location char(50)
);
commit;
COPY tw.user FROM '/USER_INFO.csv' WITH (FORMAT CSV, DELIMITER ',', ENCODING 'utf-8');
commit;

/* HASHTAGS */
create table tw.hashtags (id char(20), hashtag varchar(100));
COPY tw.hashtags FROM '/HASHTAGS.csv' WITH (FORMAT CSV, DELIMITER ',', ENCODING 'utf-8');
commit;

/* @ */
create table tw.mentions (id char(20), mention char(20));
COPY tw.mentions FROM '/MENTIONS.csv' WITH (FORMAT CSV, DELIMITER ',', ENCODING 'utf-8');
commit;

/* RETWEETS */
CREATE TABLE tw.retweets (tweet_id char(20), created_time TIMESTAMP(30), message varchar(200),
  location char(30),user_id char(20), retweet_id char(20));
commit;
COPY tw.retweets from '/retweets2.csv' WITH (FORMAT CSV, DELIMITER ',', ENCODING 'utf-8');
commit;

/* ———————————————————————————————————————— */
/* Queries */

/* Users with most tweets in the dataset */
SELECT name, n_tweets FROM
 (SELECT user_id, count(*) as n_tweets from tw.tweets group by 1 order by 2 DESC) AS Q1
LEFT JOIN
 (SELECT distinct id, name from tw.user) as Q2
ON Q1.user_id = Q2.id
ORDER BY 2 DESC;

/* Users with most followers */
SELECT name, max(followers_count) FROM tw.user group by 1 order by 2 DESC;

/* Sentiment analysis */
Select created_time, 'POSITIVE' as sent from tw.tweets where message ilike '%good%' order by 1 ASC;
Select created_time, 'NEGATIVE' as sent from tw.tweets where message ilike '%bad%' order by 1 ASC;

Copy (Select created_time, 'POSITIVE' as sent from tw.tweets where message ilike '%best%' order by 1 ASC) To '/Users/jaime/Google Drive/USF/MSAN_692_Data_Acquisition/Project/test3.csv' With CSV;
Copy (Select created_time, 'NEGATIVE' as sent from tw.tweets where message ilike '%worst%' order by 1 ASC) To '/Users/jaime/Google Drive/USF/MSAN_692_Data_Acquisition/Project/test4.csv' With CSV;


