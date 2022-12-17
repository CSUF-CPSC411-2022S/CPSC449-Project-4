# Wordle Backend Project 4 : API Endpoints

Group 4 team members:

Justin Galvez
Mark Carbajal
Juan Sierra


Steps to run the project:

1. Ensure that your nginx is configured to our tutorial.txt 

2. Open cronjob-config and paste the script into the crontab config to schedule the command.

3. Start the API by running

   foreman start

4. After the API has started, run the following to initalize the databases

   ./bin/init.sh

5. Go to local.gd docs to view and test all the endpoints

   Users Microservice: 

   http://wordle.local.gd:5000/docs#/
   EX: CREATE NEW USER
   http http://wordle.local.gd:5000/users/ first_name=jane last_name=doe password=1234 user_name=janedoe

   Leaderboard Microservice:
   http://wordle.local.gd:5100/docs#/

   Games Microservice:
   
   http://wordle.local.gd:5200/docs#/
   http://wordle.local.gd:5300/docs#/
   http://wordle.local.gd:5400/docs#/
   EX: CREATE A NEW GAME
   http -a janedoe:1234 POST http://wordle.local.gd:5400/games/
   EX: LIST IN PROGRESS GAMES
   http -a janedoe:1234 http://wordle.local.gd:5400/games/all




