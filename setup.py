from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='fresh-script',
    version='0.0.dev1',
    description='''Search for Spotify tracks posted in the HipHopHeads
                   subreddit and add them to a playlist of your choice''',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/amcquade/fresh_script',
    author='Aaron McQuade',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='spotify reddit subreddit HipHopHeads hiphop rap',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    python_requires='>=3.7',

    install_requires=['praw', 'spotipy', 'configparser', 'cutie', 'crontab', 'flask'],

    extras_require={
        'dev': ['pylint'],
    },
)
