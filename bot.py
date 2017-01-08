"""
This bot randomly upvotes posts
It upvotes a random post from the most recent [numPostsToConsider]
"""
import sys
import datetime
import os
import subprocess
from piston.steem import Steem
from random import randint

# grab config vars
percentChanceToPost = int(os.environ.get('percentChanceToPost'))
numPostsToConsider = int(os.environ.get('numPostsToConsider'))
voteWeight = int(os.environ.get('voteWeight'))
steemPostingKey = os.environ.get('steemPostingKey')
steemAccountName = os.environ.get('steemAccountName')

# [percentChanceToPost] chance to proceed past this block
i = randint(1, 100)
if i > percentChanceToPost:
    print('[{:%Y-%m-%d, %H:%M:%S}] No action (failed random roll {}>{})\n'.format(datetime.datetime.now(), i, percentChanceToPost))
    sys.exit(1)

# initialize steem object
steem = Steem(wif=steemPostingKey)

# use piston to set default voter and author
subprocess.call(['piston', 'set', 'default_voter', steemAccountName])
subprocess.call(['piston', 'set', 'default_author', steemAccountName])

# upvote random post from the most recent [numPostsToConsider]
posts = steem.get_posts(limit=numPostsToConsider, sort='created')
postId = randint(0, numPostsToConsider-1)

try:
    steem.vote(posts[postId]["identifier"], voteWeight)
except:
    print('[{:%Y-%m-%d, %H:%M:%S}] Vote failed: {}\n'.format(datetime.datetime.now(), sys.exc_info()[0]))
else:
    print('[{:%Y-%m-%d, %H:%M:%S}] Vote succeeded: {}\n'.format(datetime.datetime.now(), posts[postId]["identifier"]))   
