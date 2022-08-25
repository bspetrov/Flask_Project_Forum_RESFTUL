This application is a Flask RESTful based Forum.
It has the basic functions of an online forum. You can create threads, comment threads and like threads.
There is a manager role in the forum whom can close a specific thread if the user reports that he wants
to close the thread.
This project is based on my Django Template based self-learning porject "forumy" deployed on Heroku
- can be found here -> http://forumy-app.herokuapp.com 

Some things might differ from the Django app as my time was really limited due to personal reasons.
Its not anything special but I've tried my best.


**********************************************************************************************

Install dependencies:

- Open terminal in project root dir
- Run "pip install -r requirements.txt"

***********************************************************************************************

Endpoints:
-- Register endpoint - "/register/" - POST -- Registers a forum user (To test out the Amazon SES, use "pothednb@gmail.com" 
as this is the current verified email from the SES sandbox - returns token and message

-- Login forum user endpoint - "/login/forum_user/" -POST  - Logs in the forum user - returns token and message
-- Login forum manager endpoint - "/login/manager/" - - POST - Logs in the forum manager - returns token and message
-- Get all threads - "/thread/" - GET -- gets all threads created and their comments.

** PROTECTED - NEED TOKEN **

-- Create thread - "/thread/" - POST - returns created thread
-- Get single thread - "/thread/get/<id>/" - POST - returns thread requested
-- Comment thread - "/thread/comment/<id>/" - POST - returns thread and its comments
-- Like thread - "/thread/like/<id>/" - POST - returns thread liked
-- Dislike thread - "/thread/dislike/<id>/" - POST - returns thread disliked
-- Update thread - "/thread/update-data/<id>/" - POST - returns thread updated
-- Delete thread - "/thread/<id>/" - POST - returns a message that thread is deleted
-- Update thread status - "/thread/<id>/" - POST - returns thread with its new status
-- Get single comment - "/comment/get/<id>/" - GET - returns comment
-- Edit single comment - "/comment/edit/<id>/" - PUT - edits comment
-- Like a single comment - "/comment/like/<id>/" - PUT - likes a comment
-- Remove like from single comment - "/comment/dislike/<id>/" - PUT - removes like from comment
-- Delete single comment - "/comment/delete/<id>/" - DEL - deletes a comment

*************************************************************************************************


