# BMIS-444-Project-1
Baseball Database

Description:
This is a system that is designed to help a baseball coach keep track of team data. It tracks player information, game schedules, and every individual player's performance. I thought this would be an interesting database to make because any coach could use it for their Little League or even high school team. There is a lot of data in baseball, and without a database like this, it is very hard to keep track of. 


ERD:
![ERD](erd.png)

Table Descriptions:
- players: Stores the team roster (name, number, position, etc.)
- games: tracks the season schedule(game data, opponent)
- player_stats: This is the bridge table between players and games. It tracks the statistics for each player in each game.

For someone to run the app on their device, they would need to first install Python. The user would need to use the repository on GitHub. They would also need to set up the connection string for the database as DB_URL. 

Link:
https://baseballrosterapppy-q7eo5zoswrttequgs3snjl.streamlit.app/
