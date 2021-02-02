import praw
import threading
import math

timeframe = "all"
sorting = "controversial"


reddit = praw.Reddit(
    client_id='__F4C-ACpA-e-w',
    client_secret='DpVcitD5JHp5LRU3ZAc_PfRwUOM',
    user_agent="deepsearch and pee"
)

reddit_name = input("Enter sub name (Multiple subreddits can be combined with a +):").strip()

user_f = open("{}_users.log".format(reddit_name), "a")
reddit_f = open("{}_subs.log".format(reddit_name), "a")


def GetUsersFormComments(comments):
    print("Got {} comments".format(len(comments)))
    for comment in comments:
        try:
        
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


def GetUsers(submissions):
    for submission in submissions:
        try:
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

            #GetUsersFormComments
            data = [x for x in submission.comments.list()]
            thread_num = 8

            if len(data)>0:
                class_size = math.ceil(len(data)/thread_num)
                classes = [data[x:x+class_size] for x in range(0, len(data), class_size)]

                gu_threads = []
                for i in range(len(classes)):
                    thread = threading.Thread(target=GetUsersFormComments,args=(classes[i],))
                    gu_threads.append(thread)

                for thread in gu_threads:
                    thread.start()

                for thread in gu_threads:
                    thread.join()
                 
        except Exception as e:
            print(str(e))



#GetUsers
users = []

data = [x for x in reddit.subreddit(reddit_name).controversial(timeframe, limit=None)]
thread_num = 8

if len(data)>0:
    class_size = math.ceil(len(data)/thread_num)
    classes = [data[x:x+class_size] for x in range(0, len(data), class_size)]

    threads = []
    for i in range(len(classes)):
        thread = threading.Thread(target=GetUsers,args=(classes[i],))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()




def GetReddits(comments):
    for comment in comments:
        try:
        
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


def GetUserComments(users):
    for user in users:
        try: 
            LOGSTRING = "User: {} - Engagement: {} - Karma: {} - Link: {}".format(
                user["author"].name,
                user["num"],
                user["author"].link_karma + user["author"].comment_karma,
                "https://www.reddit.com/user/"+user["author"].name
                )
            print("\n"+LOGSTRING)
            user_f.write(LOGSTRING+"\n")


            #GetReddits
            data = [x for x in user["author"].hot(limit=None)]
            thread_num = 8

            if len(data)>0:
                class_size = math.ceil(len(data)/thread_num)
                classes = [data[x:x+class_size] for x in range(0, len(data), class_size)]

                threads = []
                for i in range(len(classes)):
                    thread = threading.Thread(target=GetReddits,args=(classes[i],))
                    threads.append(thread)

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

        except Exception as e:
            print(str(e))

        

#Filter Users
forbidden_users = ["AutoModerator", "MaxImageBot", "OwO_Bot"]
filtered_users = [u for u in users if u["author"].name not in forbidden_users or "bot" not in u["author"].name.lower()]
sorted_users = sorted(filtered_users, key=lambda x: x["num"])

#GetUserComments
reddits = []

data = sorted_users
thread_num = 16

if len(data)>0:
    class_size = math.ceil(len(data)/thread_num)
    classes = [data[x:x+class_size] for x in range(0, len(data), class_size)]


    threads = []
    for i in range(len(classes)):
        thread = threading.Thread(target=GetUserComments,args=(classes[i],))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()



    



def GetRedditInfo(reddits):
    for reddit in reddits:
        try:
            LOGSTRING = "Reddit: {} - Interactions: {} - NSFW: {} - Link: {}".format(
                reddit["reddit"].display_name,
                reddit["num"],
                reddit["reddit"].over18,
                "https://www.reddit.com/r/"+reddit["reddit"].display_name )
            print("\n"+LOGSTRING)
            reddit_f.write(LOGSTRING+"\n")
        
        except Exception as e:
                print(str(e))


#Filter
sorted_reddits = sorted(reddits, key=lambda x: x["num"])

#GetRedditInfo
data = sorted_reddits
thread_num = 16

if len(data)>0:
    class_size = math.ceil(len(data)/thread_num)
    classes = [data[x:x+class_size] for x in range(0, len(data), class_size)]


    threads = []
    for i in range(len(classes)):
        thread = threading.Thread(target=GetRedditInfo,args=(classes[i],))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()