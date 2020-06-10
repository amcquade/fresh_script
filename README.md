# fresh_script

Join us on Discord if you have anything to ask or discuss here : https://discord.gg/ZAR9ZSp

This program will search for spotify tracks posted in the HipHopHeads subreddit and add them to a playlist of your choice. HipHopHeads is a subreddit dedicated to everything hiphop, including the latest mixtapes, videos, news, and anything else hip hop related from your favorite artists.

## Getting Started

### Prerequisites

To set up this sciprt, you will need to install the following:
- Python3
- Spotify Developer Account
- Reddit Account
- Any code editor
o I recommend Visual Studio Code (https://code.visualstudio.com/)

### How to install Python3

In order to run this script, you must have Python installed on your device. 

** For Windows **  
1.Visit https://www.python.org/downloads/windows/ and download the installer for your system
2. Run the installer


** For macOS **

Note: macOS users will need to download Homebrew, in order to install Python

1. To install Homebrew, open a ‘Terminal.app” window
2. Paste the below link to install Homebrew:

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

3. In your terminal, type the following: 

brew install python3


### How to set up your Spotify Developer Account

You will need to setup a Spotify developer account. This account will share the username and password sas your regular Spotify account.  You can register here: https://developer.spotify.com/
1. Click ‘CREATE A CLIENT ID’
2. Fill out the form
3. Copy the “Client ID”
4. Click “SHOW CLIENT SECRET”
5. Copy the “CLIENT SECRET” id code.
6. Create or choose any URL to redirect to for authentication, i.e. http://google.com/
	* this must be added under your app settings > Redirect URIs 

### How to set up your Reddit Account

You will need to have a Reddit Account.  Please sign up at here:
https://www.reddit.com/register/

After signing up follow these instructions:

1. Visit https://www.reddit.com/prefs/apps/
2. Select “create another app…”
3. Fill out the form as desired
4. Copy the client id (located under your created app name)
5. Copy the secret id


## Download the repository

The repository need to be downloaded onto your system in order to run. 

1. Visit the Fresh Script Github : https://github.com/amcquade/fresh_script
2.  Click the “Clone or download” button and select “Download ZIP”
3.  Open the ZIP file and extract the folder onto your computer


### Setup your Credentials

Set up your credentials using your code editor.  Create a new file called `credentials.json` with the following contents:

```
{
    "spotify": {
        "username": "[Spotify username]",
        "client_id": "[Spotify client id]",
        "client_secret": "[Spotify client secret]",
        "redirect": "[redirect uri]"
    },
    "reddit": {
        "username": "[reddit username]",
        "client_id": "[praw client id]",
        "client_secret": "[praw client secret]"
    }
}
```

Save this file to the same folder as your local repository from the ZIP file. 

 
### Installing dependencies

You will have to run steps 1 and 2 to set up the environment.

1. Open the Command Prompt or Terminal App 
2. Type the following depending on your systems:

‘pip install --user pipenv’

### Running the script

In your Command Prompt or Terminal App:

1. Type in : ‘pipenv shell’
2. Type in : ‘python3 fresh.py’ or ‘python fresh.py’
3. Copy the link from the browser popup and enter it into the prompt
4. Choose the playlist that you would like to update
5. Enter the amount of songs you would like to add to the playlist
6. Choose the sorting method for the playlist order
7. Indicate if you would like to add songs with the “Fresh” tag
8. Refresh your Spotify app or site
9. Enjoy your new music!



Running the script using cron
We can use cron to automatically run the script periodically in order to keep it up-to-date. You will need either a macOS computer or Linux server to use cron.

Follow the running the script instructions to make sure your .config.ini file is generated with the required parameters
Run crontab -e to open the cron editor, which is similar to vim
Use the following format to create a line for your cron
* * * * * command to be executed
- - - - -
| | | | |
| | | | ----- Day of week (0 - 7) (Sunday=0 or 7)
| | | ------- Month (1 - 12)
| | --------- Day of month (1 - 31)
| ----------- Hour (0 - 23)
------------- Minute (0 - 59)
For example, you would do the following to run this everyday at 9AM
0 9 * * * python /home/jsmith/fresh.py

## Contributing

I appreciate any help and support. Feel free to [fork](https://github.com/amcquade/fresh_script#fork-destination-box) and [create a pull request](https://github.com/amcquade/fresh_script/compare)

