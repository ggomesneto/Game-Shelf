    Project Proposal – Capstone 1

The idea:
 A website for gamers in which they would search for information about a game and on return receives current information from two API and also Twitch channels streaming the game. The user could also search for genre and platforms.

1. What goal will your website be designed to achieve?
-The idea is to have all information in one place, instead of having to search in different sites for info about a game

2. What kind of users will visit your site? In other words, what is the demographic of your users?
	-Games searching for information about a specific game or even looking for new games would use the site

3. What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.
	- RAWG API contains the gaming data. TWITCH API returns data from channels being streamed. STEAM API returns the price a game is being sold. Metacritic API can be used as backup for RAWG

4. In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). 
	- At first I'll focus on the front-end to have is as user friendly as possible. Then I'll check the responses for each API to get the information needed. The idea is to have a login page so the user can save his/her searches and save some gaming data, so I`ll also have to work on sending this data to a database.

Answer questions like the ones below, but feel free to add more information:
a. What does your database schema look like?
	- At first, the data saved on a database would be something like:
    
    user = {
        id,
        password,
        saved_searches,
        collection
    }

b. What kinds of issues might you run into with your API?
	- Some information can return as null, such as streaming channels for an specific game. I`d have to handle those types of errors and add something else to the page

c. Is there any sensitive information you need to secure?
	- Passwords from each user account

d. What functionality will your app include?

e. What will the user flow look like?
- Main page of site would display a list of games based on their MetaCritic Score
- User doesn’t have to be logged in to search or use the list being showed.
- Hovering on game cards being displayed would show more information about the game and a button to even more data.
- Clicking the button would open a modal with all info + Twitch channels
-If logged in, a button would be added to the game card, to save the game to collections.

