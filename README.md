# fresh_script

This program will search for spotify tracks posted in the HipHopHeads subreddit and add them to a playlist of your choice. HipHopHeads is a subreddit dedicated to everything hiphop, including the latest mixtapes, videos, news, and anything else hip hop related from your favorite artists.

## Getting Started

### Prerequisites

This project uses Python3. You will need to setup a Spotify developer account and register your app. You will need the following things for this code:
* client id
* client secret
* your spotify username
* playlist id of the playlist you want to add the tracks to
* the url you want to redirect to for authentication, i.e. http://google.com/
 You will also need to setup a reddit instance with praw. [Heres](https://pythonforengineers.com/build-a-reddit-bot-part-1/) a useful guide I used to do this. 
```
pip3 install praw
pip3 install spotipy
pip3 install configparser
```

### Running the script

Running the program is simple. The first time you run it, you will be asked for your Spotify credientials which will be saved to a config file for ease of use in the future. Choose to sort results by hot or new, enter a post limit, and then enjoy.

```
python fresh.py
```
## Contributing

I appreciate any help and support. Feel free to [fork](https://github.com/amcquade/fresh_script#fork-destination-box) and [create a pull request](https://github.com/amcquade/fresh_script/compare)
