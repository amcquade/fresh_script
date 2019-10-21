from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

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
        'Topic :: Software :: Music Tools',
    ],

    keywords='spotify reddit HipHopHeads hiphop music',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    python_requires='>=3.7',

    install_requires=['praw', 'spotipy', 'configparser', 'cutie', 'crontab', 'flask'],

    extras_require={
        'dev': ['pylint'],
    },

    project_urls={
        'Bug Reports': 'https://github.com/amcquade/fresh_script/issues',
        'Source': 'https://github.com/amcquade/fresh_script',
    },
)
