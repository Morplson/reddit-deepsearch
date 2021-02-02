import praw

reddit = praw.Reddit(
    client_id='__F4C-ACpA-e-w',
    client_secret='DpVcitD5JHp5LRU3ZAc_PfRwUOM',
    user_agent="deepsearch and pee"
)




reddit_name = input("Enter sub name (Multiple subreddits can be combined with a +):").strip()

user_f = open("{}_users.log".format(reddit_name), "a")
reddit_f = open("{}_subs.log".format(reddit_name), "a")


users = []
for submission in reddit.subreddit(reddit_name).controversial("all", limit=None):
    print("\nPost: {} {} - {}".format(submission.title,submission.score,submission.url))

    #Submission Poster
    user = submission.author
        
    if(user):
        res = next((item for item in users if item['author'] == user), None)

        if(not res):
            users.append({"author":user,"num":1})
        else:
            res["num"] += 1
    else:
        print("An error occured: https://www.reddit.com{}".format(submission.permalink))

    try:
        comments = submission.comments.list()
        print("Got {} comments".format(len(comments)))
        for comment in comments:
            print(comment.body)

            #Comment Poster
            user = comment.author
            
            if(user):
                res = next((item for item in users if item['author'] == user), None)

                if(not res):
                    users.append({"author":user,"num":1})
                else:
                    res["num"] += 1
            else:
                print("An error occured: https://www.reddit.com{}".format(comment.permalink))
    except Exception as e:
        print(str(e))


#Filter Users
forbidden_users = ["AutoModerator", "MaxImageBot", "OwO_Bot"]
filtered_users = [u for u in users if u["author"].name not in forbidden_users or "bot" not in u["author"].name.lower()]

reddits = []
for user in filtered_users:
    try:
        LOGSTRING = "User: {} - Engagement: {} - Karma: {} - Link: {}".format(
            user["author"].name,
            user["num"],
            user["author"].link_karma + user["author"].comment_karma,
            "https://www.reddit.com/user/"+user["author"].name
            )
        print("\n"+LOGSTRING)
        user_f.write(LOGSTRING+"\n")

    
        for comment in user["author"].controversial("all", limit=None):
            sub = comment.subreddit

            if(sub):
                res = next((item for item in reddits if item['reddit'] == sub), None)

                if(not res):
                    reddits.append({"reddit":sub,"num":1})
                else:
                    res["num"] += 1
            else:
                print("An error occured: https://www.reddit.com{}".format(comment.permalink))
    except Exception as e:
        print(str(e))

for reddit in reddits:
    LOGSTRING = "Reddit: {} - Interactions: {} - NSFW: {} - Link: {}".format(
        reddit["reddit"].display_name,
        reddit["num"],
        reddit["reddit"].over18,
        "https://www.reddit.com/r/"+reddit["reddit"].display_name )
    print("\n"+LOGSTRING)
    reddit_f.write(LOGSTRING+"\n")