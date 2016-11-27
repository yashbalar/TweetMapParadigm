# Scalable TweetMap by Yash Balar and Vivek Ghatala

The web application collect Tweets, do some processing and represent the Tweets on GoogleMaps.

- Used Twitter Streaming API to fetch tweets from the twitter hose in real-time

- Used SQS and SNS with Alchemy API to analyze sentiment of the real time incoming tweets

- Used ElasticSearch to store tweets in backend

- Created a web app using Django that allows users to search for a few keywords

- Used Google Maps API to render these filtered tweets on the map

- Deployed the application on AWS Elastic Beanstalk in an auto-scaling environment
