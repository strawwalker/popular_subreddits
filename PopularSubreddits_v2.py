#! python3
#   Grabs the most popular subreddits and places the subreddit name, subscriber
#   number, top 30 post scores, and newest post scores up to 30 days old, into
#   a csv file. Includes a count of submissions over the last 1 and 2 days.

import praw, datetime

SAMPLES = 5000    #Set how many subreddits to grab, 5000 is the maximum.
TOP = 30          #Set how many top posts to grab scores from.
NEW = 30          #Set how many days worth of new posts to grab scores from.

reddit = praw.Reddit(client_id='client id',client_secret='client secret',user_agent='user agent')

now = datetime.datetime.utcnow()
index = 0
comma_sep_list = ['rank,subreddit,createdUTC,age(days),subscribers,top '+str(TOP)+' post scores']
for i in range(TOP):
    comma_sep_list.append(',')
comma_sep_list.append('#Posts less than 1 day old,#Posts less than 2 days old,Post scores(last '+str(NEW)+' days)\n')

for subreddit in reddit.subreddits.popular(limit = SAMPLES):
    try:
        csTopPostScore = ''
        csNewPostScore = ''
        csNewPostCount = 0
        csNewestPostCount = 0
        for submission in subreddit.top(limit=TOP):
            csTopPostScore = str(csTopPostScore)+','+str(submission.score)
        for submission in subreddit.new(limit=None):
            submissionAge = (now - datetime.datetime.utcfromtimestamp(submission.created_utc)).days
            if submissionAge < 2:
                csNewPostCount += 1
                if submissionAge < 1:
                    csNewestPostCount +=1
            if submissionAge > NEW:
                break
            csNewPostScore = csNewPostScore+','+str(submission.score)
        index += 1
        csTopPostScore = csTopPostScore[1:]
        csNewPostScore = csNewPostScore[1:]
        csCreated = datetime.datetime.utcfromtimestamp(subreddit.created_utc).isoformat()
        csAge = (now - datetime.datetime.utcfromtimestamp(subreddit.created_utc)).days
        csSubscribers = subreddit.subscribers
        subVals = ','.join([str(index),str(subreddit),str(csCreated),str(csAge),str(csSubscribers),str(csTopPostScore),str(csNewestPostCount),str(csNewPostCount),str(csNewPostScore)])
        comma_sep_list.append(subVals)
        comma_sep_list.append('\n')
        if (index)%250 == 0:
            print(''.join([str(round((index/SAMPLES)*100,3)),'%']))
    except:
        print('An error occurred getting values for '+str(subreddit)+'. Subreddit was omitted from the list.')
    
csv = ''.join(comma_sep_list)
print()
print(index,'subreddits were grabbed.')

subRandSampFile = open('C:\\directory\\Popular_Subreddits.csv','w')
subRandSampFile.write(csv)
subRandSampFile.close()
