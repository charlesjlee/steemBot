

## Steem for the people
When someone writes a great post on Reddit that goes viral and is widely shared, the party that benefits most is Reddit itself. Realizing this and wanting to give back to the community responsible for its success, Reddit toyed with the idea of giving shares of the company to users in the form of a cryptocurrency. This plan was later [put on indefinite hold](http://www.theverge.com/2015/2/3/7968397/reddit-backtracks-reddit-notes-cryptocurrency).

[Steem](https://steem.io) is the embodiment of what Reddit wanted to achieve -- a blockchain-based, social news platform where posters and upvoters, i.e. "curators", are rewarded directly with cryptocurrency (actually three currencies: STEEM, Steem Power, and Steem Dollars). I was first exposed to Steem via [Steemit](https://steemit.com), a website built on top of the Steem blockchain. My first thought after learning about Steemit and reading the white paper was "wouldn't it be neat if I could write a bot that would 'curate', upvote posts for me, and make me rich overnight?" Of course, it wasn't that easy, but at least no one can say I didn't *try* to get rich quick.

This is a guide to creating a simple bot that will periodically upvote a random post. Specifically, the bot will work like this (numbers are configurable):

1. Bot will wake up every 10 minutes, but only run 5% of the time. This is to give new posts a chance to appear and to preserve voting power
2. If the bot runs, it will randomly upvote one of the 20 most recent posts with weight 100. The weight can be adjusted if you want to experiment with voting more often but with less weight. Every vote decreases your voting power, which regenerates over time, and hence the rewards you can potentially earn

Our bot will be built using GitHub, Heroku, and [@xeroc](https://steemit.com/@xeroc)'s excellent Steem library, [steem-piston](https://github.com/xeroc/piston). We'll build this in two steps: 

1. Create accounts (will need email, cellphone, credit card)
2. Setup and deploy Heroku project

## 1) Create accounts

### Create [Heroku](https://www.heroku.com) account
The first step is to create an account on [Heroku](https://www.heroku.com). *Dynos* are the Heroku term for virtual machine instances. You initially start with 550 free dyno hours. If you add a credit card number, you get an additional 450 free hours and the ability to use free add-ons. We will be using the free Scheduler add-on to make our bot run every 10 minutes, so add your credit card number now.

If you didn't add your credit card during registration, you can do so after you login:  
Click your avatar in the upper right-hand corner --> Account settings --> Billing

### Create [SteemIt](https://steemit.com) account
Next you need an account on the Steem blockchain (this costs a fee). The easiest way to do this is to register an account on [Steemit](https://steemit.com), a website that runs on top of Steem to display its contents (Steemit will pay the fee). To help combat account creation abuse, Steemit recently switched from a [Facebook/Reddit](https://steemit.com/steemit/@gord0b/abusing-steemit-using-facebook-sign-up) registration process to an email + SMS process.

After you finish registering, log into your Steemit account and grab your private Posting key. You can find this by going to the URL below and clicking **Show Private Key** next to **Posting**. Our bot will need this key to vote on our behalf.  
https://steemit.com/@ReplaceWithYourSteemHandle/permissions

### Create [GitHub](https://github.com/join) account
Git is a version control system for tracking changes to files and coordinating work on those files among multiple people. [GitHub](https://github.com/join) is a popular web-based service that hosts Git repositories. We will use GitHub to store our code in a repository and then point Heroku to that repository.

## 2) Setup and deploy Heroku project
### Fork GitHub repo
What is a _fork_?

>> A _fork_ is a copy of a repository. Forking a repository allows you to freely experiment with changes without affecting the original project.
https://help.github.com/articles/fork-a-repo/

In this case, you'll fork my repository by clicking the link below, logging into your GitHub account, and clicking the **Fork** button in the upper right-hand corner.  
https://github.com/charlesjlee/steemBot

### Create Heroku project and link to GitHub
Now we're ready to create our Heroku project:

1. Log into Heroku and go to the app dashboard  
https://dashboard.heroku.com/apps
2. Click **New** in the upper right-hand corner then **Create new app**. You can give the app a name or leave it blank to randomly generate one. Click **Create App**. This brings you to the app configuration site
3. You should be in the **Deploy** tab. If not, then click **Deploy** to navigate there. Under **Deployment method**, click **GitHub**. The bottom items will refresh and you will only see the **Connect to GitHub** item. Click that, enter your GitHub password, and **Connect** to the `steemBot` repository you just forked
4. Now **Connect to GitHub** disappears and is replaced with other items. Under **Manual deploy**, click **Deploy Branch**. This tells Heroku to pick-up the code in the repository we just linked and compile it into a slug, Heroku's term for a runnable package

### Setup config vars
Let's set some custom values:

1. Navigate to the **Settings** tab and find the **Config Variables** item
2. Click **Reveal Config Vars**. There are 5 config vars we need to enter:

    |key|example value|comment|
    |---|:---:|---|
    |numPostsToConsider|20|Number of recent posts to consider|
    |percentChanceToPost|5|Percent chance that script will run. Must be between 0 and 100|
    |steemAccountName|'mySteemName'|Your Steem account name wrapped in single quotes|
    |steemPostingKey|'myPrivatePostingKey'|Your Private Posting Key that you saved when creating your SteemIt account, wrapped in single quotes|
    |voteWeight|100|How much voting power to use per upvote. Note that voting power decreases after every vote. Must be between 0 and 100|

### Schedule bot
Finally we schedule our bot using the free Heroku Scheduler Add-on:

1. Navigate to the **Resources** tab
2. Under **Add-ons**, search for **Heroku Scheduler** then click **Provision** in the pop-up
3. Now **Heroku Scheduler** appears as a row. Click it and a new window opens
4. In the new window, click **Add new job**. Enter **python bot.py** in the text box and change the **Frequency** to **Every 10 minutes**. Click **Save**

### Check logs and celebrate
That's it! Now our bot is running every 10 minutes and has a `percentChanceToPost` chance to activate. Every time the bot activates, it will choose a random post from the most recent `numPostsToConsider` and upvote it with weight `voteWeight`. You can see the run logs of your bot by going to:  
More (to the right of Open app, in the upper right corner) --> View logs

You can see your handiwork being written to the Steem block chain using this block chain explorer:
https://steemd.com/@ReplaceWithYourSteemHandle
