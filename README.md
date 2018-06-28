# fresh_script

This program will search for spotify tracks posted in the HipHopHeads subreddit 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need to setup a Spotify developer account and register your app. You will need the following things for this code:
* client id
* client secret
* your spotify username
* playlist id of the playlist you want to add the tracks to
* the url you want to redirect to for authentication, i.e. http://google.com/
 You will also need to setup a reddit instance with praw. [Heres](https://pythonforengineers.com/build-a-reddit-bot-part-1/) a useful guide I used to do this. 
```
pip install praw
pip install spotipy
```

### Running the script

Running the program is simple. The first time you run it, you will be asked for your Spotify credientials which will be saved to a config file for ease of use in the future. Choose to sort results by hot or new, enter a post limit, and then enjoy.

```
python fresh.py
```
