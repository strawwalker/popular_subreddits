#! python3
#   Grabs the most popular subreddits and places the subreddit name, subscriber
#   number, and top post score into a csv file.

import praw

SAMPLES = 5000    #Set how many subreddits to grab, 5000 is the maximum.

reddit = praw.Reddit(client_id='client id',client_secret='client secret',user_agent='user agent')

index = 0
comma_sep_list = ['subreddit,subscribers,top post score\n']

for subreddit in reddit.subreddits.popular(limit = SAMPLES):
    try:
        for submission in subreddit.top(limit=1):
            csTopPostScore = submission.score
        csSubscribers = subreddit.subscribers
        subVals = ','.join([str(subreddit),str(csSubscribers),str(csTopPostScore)])
        comma_sep_list.append(subVals)
        comma_sep_list.append('\n')
        index += 1
        if (index)%250 == 0:
            print(''.join([str(round((index/SAMPLES)*100,3)),'%']))
    except:
        print(str(subreddit)+' has no top submission')
    
csv = ''.join(comma_sep_list)
print()
print(index,'subreddits were grabbed.')

subRandSampFile = open('C:\\directory\\Popular_Subreddits.csv','w')
subRandSampFile.write(csv)
subRandSampFile.close()
