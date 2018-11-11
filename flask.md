# fresh flask

This is an extension of the script utitlizing the flask web framework.

## activate the environment

Before you work on your project, activate the corresponding environment:
```
. venv/bin/activate
pip install flask spotipy praw
```

## running flask
### linux/mac
To run the application you can either use the flask command or python’s -m switch with Flask. Before you can do that you need to tell your terminal the application to work with by exporting the FLASK_APP environment variable:
```
$ export FLASK_APP=app.py
$ flask run
 * Running on http://127.0.0.1:5000/
```
Alternatively you can use ```python -m flask```:
```
$ export FLASK_APP=app.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/
``` 
### windows
If you are on Windows, the environment variable syntax depends on command line interpreter. On Command Prompt:
```
C:\path\to\app>set FLASK_APP=hello.py
```
And on PowerShell:
```
PS C:\path\to\app> $env:FLASK_APP = "hello.py"
```

This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production.
Now head over to http://127.0.0.1:5000/, and you should see your hello world greeting.