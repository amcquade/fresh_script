from setuptools import setup

setup(
    name='fresh_script',
    version='1.2.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
    install_requires=['spotipy', 'prawcore', 'flask', 'configparser', 'constants', 'cutie', 'git', 'crontab', 'textwrap']
    url='https://github.com/amcquade/fresh_script',
    license='MIT',
    author='amcquade',
    author_email='',
    description='Find Spotify tracks posted to the HipHopHeads subreddit and add them to a Spotify playlist.'
)
