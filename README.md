# fresh_script

This program will search for spotify tracks posted in the HipHopHeads subreddit and add them to a playlist of your choice. HipHopHeads is a subreddit dedicated to everything hiphop, including the latest mixtapes, videos, news, and anything else hip hop related from your favorite artists.

# Table of Contents
[New features](https://github.com/samuel-stjean/fresh_script#new-features)
[Getting Started](https://github.com/samuel-stjean/fresh_script#getting-started)
 - [Prerequisites](https://github.com/samuel-stjean/fresh_script#prerequisites)
 - [Setup your Credentials](https://github.com/samuel-stjean/fresh_script#setup-your-credentials)
 - [Installing dependencies](https://github.com/samuel-stjean/fresh_script#installing-dependencies)
 - [Running the script](https://github.com/samuel-stjean/fresh_script#running-the-script)
 - [Script arguments](https://github.com/samuel-stjean/fresh_script#script-arguments)
 - [Running the script using cron](https://github.com/samuel-stjean/fresh_script#running-the-script-using-cron)
[Contributing](https://github.com/samuel-stjean/fresh_script#contributing)

## New Features!
[Flask](http://flask.pocoo.org/) has recently been added to the project. You can read up on how to get it setup [here](flask.md).

## Getting Started

### Prerequisites

This project uses Python3.

You will need to setup a Spotify developer account and register your app and obtain the following information:
* client id
* client secret
* your spotify username
* playlist id of the playlist you want to add the tracks to
* the url you want to redirect to for authentication, i.e. http://google.com/
  * this must be added under your app settings > Redirect URIs 

You will also need to setup a reddit instance with praw. [Here's](https://pythonforengineers.com/build-a-reddit-bot-part-1/) a useful guide I used to do this.

### Setup your Credentials

To set up your credentials, create a new file called `credentials.json` in the root of the project with the following contents:

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
 
### Installing dependencies
This project uses a dependency manager called [pipenv](https://pipenv.readthedocs.io). Follow the instructions to install it [here](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv).

The project dependencies are listed in a [Pipfile](https://github.com/pypa/pipfile). Using pipenv, you can install all the dependencies with the following commands:
```bash
cd fresh_script
pipenv install
``` 

Pipenv uses [virtualenv](https://virtualenv.pypa.io/en/stable/) to create a python environment with all the dependencies listed in the Pipfile. Before running the fresh.py script, you must first activate the environment:
```bash
pipenv shell
```

If you wish to deactivate the environment use the command
```bash
exit
```

### Running the script

Running the program is simple. The first time you run it, you will be asked for your Spotify credientials which will be saved to a config file for ease of use in the future. Choose to sort results by hot or new, enter a post limit, and then enjoy.

```
python3 fresh.py
```

### Script arguments

The following arguments can be passed to the script

| Short | Long             | Type   | Description |
|-------|------------------|--------|-------------|
| -s    | --sort           | string | Sort by hot, new, rising, random_rising, controversion or top |
| -l    | --limit          | int    | How many posts to grab |
| -t    | --threshold      | int    | Only posts with score above threshold |
| -f    | --fresh          | bool   | Only add tracks with the \[FRESH\] tag |
| -ia   | --include-albums | bool   | Include tracks from albums |
| -v    | --verbose        | bool   | Output songs being added and other info |
| -p    | --playlists      | bool   | List, add, or remove playlists to add songs to |

### Running the script using cron

We can use cron to automatically run the script periodically in order to keep it up-to-date. You will need either a macOS computer or Linux server to use cron.

1. Follow the `running the script` instructions to make sure your `.config.ini` file is generated with the required parameters
2. Run `crontab -e` to open the cron editor, which is similar to vim
3. Use the following format to create a line for your cron
    ```
    * * * * * command to be executed
    - - - - -
    | | | | |
    | | | | ----- Day of week (0 - 7) (Sunday=0 or 7)
    | | | ------- Month (1 - 12)
    | | --------- Day of month (1 - 31)
    | ----------- Hour (0 - 23)
    ------------- Minute (0 - 59)
    ```
    For example, you would do the following to run this everyday at 9AM
    ```
    0 9 * * * python /home/jsmith/fresh.py
    ```

## Contributing

1. [Fork](https://github.com/amcquade/fresh_script#fork-destination-box) the Repository: Start by forking the project's repository to your GitHub account. This creates a copy of the project that you can freely modify. [tutorial](https://www.youtube.com/watch?v=l5NrYIa_aG4&pp=ygUWZm9yayByZXBvc2l0b3J5IGdpdGh1Yg%3D%3D)

2. [Clone](https://www.youtube.com/watch?v=TBoS5Qbv89o&pp=ygUVY2xvbmUgYSBmb3JrIHRvIGxvY2Fs) Your Fork: Clone your forked repository to your local development environment using `git clone`.

3. Create a [Branch](https://www.youtube.com/watch?v=snxybJkFeUo&pp=ygUVY3JlYXRlIGEgYnJhbmNoIGxvY2Fs): Create a new branch for your contribution. Please use a descriptive name.

4. Make & Document Changes: Make your desired changes or additions to the codebase, update the documentation, comments, or README files.

5. [Commit & Push](https://www.youtube.com/watch?v=lYiE5lBS13E&pp=ygUPY29tbWl0IGFuZCBwdXNo) Your Changes: Commit your changes with a clear and concise commit message that describes what your changes accomplish and push your branch with your changes to your GitHub fork.

6. [Create a Pull Request](https://github.com/amcquade/fresh_script/compare): Go to the original project's repository and create a new Pull Request from your forked branch. Provide a clear description of your changes in the PR description.

I appreciate any help and support. Thank you! 
