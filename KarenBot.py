#! /Users/garretdonaldson/pyProjects/Bots/KarenBot/env/bin/python3

import praw
import sqlalchemy as db
import re
import random as rand
from sqlalchemy import Column, String, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import praw.exceptions


reddit = praw.Reddit('KarenBot')
# each subreddit organies by .hot, .new, .controversial, .top, and .gilded
# can also use engine search via .search("SEARCH_KEYWORDS")
karenRegex = re.compile(r'a Karen', re.IGNORECASE)

# karenList = ["Keep'm comin', pal, I went through child birth AND child death.", 
#"Michaelllllllllll!!", "You will call me by my husband's rank"]
karenList = ["You will call me by my husband's rank", 
            "Keep'm coming, pal, I went through child birth _and_ child death",
            "Um, yeah. I'm gonna have to speak to your manager...", 
            "This is not very _live love laugh_ of you. You should be ashamed of yourself.", 
            "My son's a vegetarian and you've got beef? I expect all downvotes to be removed from this order, and some free gold thrown in.", 
            "I demand this account be deleted.", 
            "I bet you were vaccinated.",
            "Think of the children",
            "How dare you, on my daughter's birthday",
            "My children were raised to be better than you"]
karenSignature = "_Beep Boop, I'm a b*tch_"


# create database connection and start it  
Base = declarative_base() # Create initial Base class to defined mapped classes from

engine = db.create_engine('sqlite:///roxy.sqlite3', echo=True) 
connection = engine.connect()
Base.metadata.create_all(engine)

# Create session object, which is the ORM's "handle" to the database, allowing conversation withi it
# use session = Session() whenever need to talk to database
Session = sessionmaker(bind=engine)

class Comment(Base):
    __tablename__ = 'comments'

    post_title = Column(String, primary_key=True)
    comment_id = Column(String, primary_key=True)
    comment_body = Column(String)
    user_id = Column(String)

    def __repr__(self):
        return "<Comments(post_title='%s', comment_id='%s', comment_body='%s', user_id='%s')>" % (
            self.post_title, self.comment_id, self.comment_body, self.user_id)



#create dummy user to test
# dummy_post = Comment(post_title='Testing my SQLite3 database!', comment_id='5h35tf',
    #comment_body='What the reddit user said!', user_id='dummyRedditUser_69')

#session = Session()
#session.add(dummy_post)
#session.commit()


blackList = [
    "talesfromyourserver",
    "bmw",
    "anime", 
    "asianamerican", 
    "askhistorians", 
    "askscience", 
    "askreddit", 
    "aww", 
    "chicagosuburbs", 
    "cosplay", 
    "cumberbitches", 
    "d3gf", 
    "deer", 
    "depression", 
    "depthhub", 
    "drinkingdollars", 
    "forwardsfromgrandma", 
    "geckos", 
    "giraffes", 
    "grindsmygears", 
    "indianfetish", 
    "me_irl", 
    "misc", 
    "movies", 
    "mixedbreeds", 
    "news", 
    "newtotf2", 
    "omaha", 
    "petstacking", 
    "pics", 
    "pigs", 
    "politicaldiscussion", 
    "politics", 
    "programmingcirclejerk", 
    "raerthdev", 
    "rants", 
    "runningcirclejerk", 
    "salvia", 
    "science", 
    "seiko", 
    "shoplifting", 
    "sketches", 
    "sociopath", 
    "suicidewatch", 
    "talesfromtechsupport",
    "torrent",
    "torrents",
    "trackers",
    "tr4shbros", 
    "unitedkingdom",
    "crucibleplaybook",
    "cassetteculture",
    "italy_SS",
    "DimmiOuija",
    "permission",
    "benfrick",
    "bsa",
    "futurology",
    "graphic_design",
    "historicalwhatif",
    "lolgrindr",
    "malifaux",
    "nfl",
    "toonami",
    "trumpet",
    "ps2ceres",
    "duelingcorner",
    "fuckyoukaren",
    "karen",
    "askteengirls",
    "londonontario"
]

subreddit = reddit.subreddit("All")

# Indefinitely iterate over submissions and comments in All
for submission in subreddit.stream.submissions():
    p_compareList = []
    if submission.subreddit not in blackList:
        postTitle = submission.title # store post title in case a match is found in next loop
        for comment in subreddit.stream.comments():
            
            # store values in case match is found, so can add to Comment table
            cBody = comment.body
            cID = comment.id
            cAuthor = comment.author.name

            karenMatch = karenRegex.search(cBody)
            exceptionList = []

            if karenMatch is None:
                continue
            else:
                print('Match found')
                session = Session()
                c_compareList = []
                for instance in session.query(Comment.comment_id):
                    c_compareList.append(instance)
                for instance in session.query(Comment.post_title):
                    p_compareList.append(instance)
                if cID not in c_compareList and postTitle not in p_compareList:
                    try:
                        comment.reply(karenList[rand.randint(0,9)] + '\n\n' + karenSignature)
                        session.add( Comment(post_title=postTitle, comment_id=cID, comment_body=cBody, user_id=cAuthor))
                        print('Replying to comment')
                    except praw.exceptions.RedditAPIException as exception:
                        for subException in exception.items:
                            exceptionList.append(subException.error_type)
                            print(exceptionList)
                            
                
                session.commit()
                print(cBody)
                print(cID)
                print(cAuthor)
                print(postTitle)


