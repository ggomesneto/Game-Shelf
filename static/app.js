// SOME VARIABLES NEED TO BE HARD CODED DUE TO THE API SCHEMA.

const BASE_URL = 'https://api.rawg.io/api';

// EACH API REQUEST SEND A LINK FOR THE 'NEXT PAGE' RESULTS. I ADDED A EMPTY VARIABLE SO I CAN USE THE DATA GLOBALLY
let nextPage = '';

// GETTING DATES FOR THE FIRST SEARCH = TRENDING ON THE LAST YEAR

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = yyyy + '-' + mm + '-' + dd;

yyyy = String(parseInt(yyyy) - 1);
let lastyear = yyyy + '-' + mm + '-' + dd;

const startSearchUrl = `https://api.rawg.io/api/games?dates=${lastyear},${today}&-ratings`;

// EACH PLATFORM HAS AN ID ON THE API. THE IDS ARE NOT IN SEQUENCE, SO I HAVE TO GET THEM ALL, FILL AN ARRAY WITH THE NAMES I WANT AND THEN CHECK THE IDS OF EACH PLATFORM INDIVIDUALLY. THE ARRAYS ARE OUT OF THE FUNCTION, SO I CAN USE THEM GLOBALLY.

let platList = [];

let platIDList = [];

// EACH PLATFORM HAS ITS OWN MARKUP FOR THE ICON FROM FONT AWESOME

const playstation = '<i class="fab fa-playstation"></i>';
const pc = '<i class="fas fa-desktop"></i>';
const xbox = '<i class="fab fa-xbox"></i>';
const nSwitch = '<i class="fab fa-neos"></i>';
const android = '<i class="fab fa-android"></i>';
const ios = '<i class="fab fa-apple"></i>';

let platIcon = [ pc, playstation, xbox, nSwitch, android, ios ];

// ---------------------------------------------- FUNCTIONS ------------------------------------------------

//THIS USES THE TITLE OF THE PAGE TO KNOW THE CORRECT GENRE TO BE SEARCHED. IT CALLS getDataGenre TO GET THE GAMES
async function getGenre() {
	$('#result_search').empty();

	let target = $('#title');
	let genreName = target.text().toLowerCase();

	if (genreName === 'rpg') {
		genreName = 'role-playing-games-rpg';
	}

	await getDataGenre(genreName);
}

// MAKES A REQUEST FOR THE GENRE, SAVES NEXTPAGE, MAPS THE RESULTS USING THE CLASS GAME, AND THEN APPEND THE RESULTS ON THE PAGE
async function getDataGenre(genreName) {
	let response = await axios.get(`${BASE_URL}/games?genres=${genreName}`);

	let gameArr = response.data.results;

	nextPage = response.data.next;

	let result = gameArr.map((game) => new Game(game));

	for (let game of result) {
		let gameHTML = generateCardHTML(game);
		$('#result_search').append(gameHTML);
	}
}

//THIS EMPTIES THE RESULTS DIV, USES THE TITLE OF THE PAGE TO KNOW WHAT NEEDS TO BE SEARCHED. IT CALLS mainSearch TO GET THE GAMES
async function searchBox() {
	$('#result_search').empty();

	let target = $('#title');
	let searchText = target.text().toLowerCase();

	await mainSearch(searchText);
}

// MAKES A REQUEST FOR THE SEARCH DATA, SAVES NEXTPAGE, MAPS THE RESULTS USING THE CLASS GAME, AND THEN APPEND THE RESULTS ON THE PAGE
async function mainSearch(searchText) {
	let response = await axios.get(`${BASE_URL}/games?search='${searchText}'`);
	let gameArr = response.data.results;
	nextPage = response.data.next;
	let result = gameArr.map((game) => new Game(game));

	for (let game of result) {
		let gameHTML = await generateCardHTML(game);
		$('#result_search').append(gameHTML);
	}
}

// MAKES A REQUEST TO GET THE PLATFORMS LIST.
//  - MAP THE RESULTS
//  - GETS ALL THE PLATFORMS ON THE MENUS, USING THE CLASS .PLATFORMS
//  - COMPARE THE LIST FROM THE REQUEST WITH THE LIST FROM THE CLASSES AND GET THE IDS FOR THE PLATFORMS THAT MATCH

async function getPlatInfo() {
	let response = await axios.get('https://api.rawg.io/api/platforms');
	let result = response.data.results;
	let platformsInfo = result.map((platform) => [ platform.name.toLowerCase(), platform.id ]);

	let $platforms = $('.platform');

	for (platform of $platforms) {
		platList.push(platform.innerText.toLowerCase());
	}

	for (plat of platList) {
		for (i = 0; i < platformsInfo.length; i++) {
			if (plat === platformsInfo[i][0]) {
				platIDList.push(platformsInfo[i][1]);
			}
		}
	}
}

//THIS EMPTIES THE RESULTS DIV, USES THE TITLE OF THE PAGE TO KNOW WHAT NEEDS TO BE SEARCHED. IT CALLS getDataPlat TO GET THE GAMES
async function getPlatform() {
	$('#result_search').empty();

	let target = $('#title');
	let platName = target.text().toLowerCase();

	await getDataPlat(platName);
}

//  - AWAITS FOR getPlatInfo SO IT CAN USE THE ID LISTS
//  - USES THE PLATFORM ID LIST TO GET THE CORRECT ID BASED IN WHAT NEEDS TO BE SEARCHED
//  - MAKES A REQUEST WITH THE CORRECT ID
//  - MAP IT USING THE CLASS GAME
//  - APPEND TO THE PAGE

async function getDataPlat(platName) {
	let platID = '';

	await getPlatInfo();

	platID = platIDList[platList.indexOf(platName)];

	let response = await axios.get(`${BASE_URL}/games?platforms=${platID}`);

	let gameArr = response.data.results;
	nextPage = response.data.next;

	let result = gameArr.map((game) => new Game(game));

	for (let game of result) {
		let gameHTML = generateCardHTML(game);
		$('#result_search').append(gameHTML);
	}
}

// PRIMARY SEARCH FOR WHEN YOU OPEN THE MAIN PAGE - USES THE STARTSEARCHURL.
async function startSearch() {
	let response = await axios.get(`${startSearchUrl}`);
	let gameArr = response.data.results;
	nextPage = response.data.next;
	let result = gameArr.map((game) => new Game(game));

	for (let game of result) {
		let gameHTML = await generateCardHTML(game);
		$('#result_search').append(gameHTML);
	}
}

//CREATES THE MARKUP FOR EACH GAME CARD
async function generateCardHTML(game) {
	let gameName = game.name;
	let gameRel = game.released;
	let gameImg = game.image;
	let metacritic = game.metacritic;
	let platforms = game.platforms;
	let slug = game.slug;
	let genres = game.genres;

	// CHECK IF THE API HAS A METACRITIC SCORE. IF NOT, SET IT TO 'NA'
	if (metacritic === null) {
		metacritic = 'NA';
	}

	// EACH GAME HAS DIFFERENT PLATFORMS. THIS FOR LOOP IS TO CHECK THE PLATFORMS THE GAME HAS AND ADD THE ICON REFERRED TO THE PLATFORM TO THE MARKUP.
	let icon = '';

	for (platform of platforms) {
		let index = platList.indexOf(platform.toLowerCase());
		if (index === -1) {
		} else {
			let iconHTML = platIcon[index];

			if (icon.includes(iconHTML)) {
			} else {
				icon = icon.concat(iconHTML);
			}
		}
	}

	// CHECK IF USER IS LOGGED IN. IF YES, GET THE LIST OF THE USER'S FAVORITED GAME AND MODIFY THE MARKUP IF THE GAME IS IN THE USER'S COLLECTION OR NOT.
	let response = await axios.get(`/islogged`);

	let data = response.data;
	let slugList = data.game_slug;

	if (data.islogged === true) {
		if (slugList.includes(slug)) {
			favIcon = `<button class='btn btn-danger addFav' data-game-slug=${slug} id='favorite'>X</button>`;
		} else {
			favIcon = `<button class='btn btn-success addFav' data-game-slug=${slug} id='favorite'>+</button>`;
		}
	} else {
		favIcon = `<a href='/login'><button class='btn btn-success addFav' data-game-slug=${slug}>+</button></a>`;
	}

	// EACH GAME CAN HAVE MULTIPLE GENRES. THIS FOR LOOP CHECKS ALL GENRES AND CONCATENATES THEM TOGETHER ON THE MARKUP
	let markupList = '';

	for (g of genres) {
		if (g.name === 'Massively Multiplayer') {
			g.name = 'MMO';
		}
		let genreSlug = g.name.toLowerCase();

		let genre_markup = `<a href='/genres/${genreSlug}' class='genre'><span class='card-data mr-1'>${g.name}</span></a>`;
		markupList = markupList + genre_markup;
	}
	// GAME CARD THAT WILL BE APPENDED ON THE HTML
	const gameMarkup = $(`
    
    
        <div class="col card_search">
		
					<div class="card">
					
					
                        <img class="card-img-top" src="${gameImg}" alt="Card image cap">
                        <div class="card-body">
                            <div class='container-fluid icons'>
                               ${icon}
                                <i class='btn btn-success p-1 score '>${metacritic}</i>
                            </div> 
                            <a href='/games/${slug}'><h5 class="card-title">${gameName}</h5></a>

							<div class='text-center'>
							<a href='/games/${slug}/review'><button class='btn btn-dark' id='add-review'>ADD REVIEW</button></a>${favIcon}
                            </div>

                            <ul class=" list-group-flush card_list">
                                <li class="list-group-item">Release Date:<span class='card-data'>${gameRel}</span></li>
                                <li class="list-group-item">Genre:<small>${markupList}</small></li>
                                
								
                            </ul>
                        </div>
                    </div>
                    
        </div>
    
    `);

	return gameMarkup;
}

// THIS FUNCTION CREATES A FOR LOOP TO GET THE COLLECTION FROM THE USER.
async function getCollection(id, user_logged) {
	let response = await axios.get(`/api/${id}/collection`);

	let collection = response.data.collection;
	let collectionArr = [];

	// MAKES A FOR LOOP REQUESTING THE DATA FROM EACH GAME TO THE API.
	for (game of collection) {
		let apiCall = await axios.get(`${BASE_URL}/games/${game.game_slug}`);
		collectionArr.push(apiCall.data);
	}

	// MAPS THE GAMES AND RUN THEN ON THE CLASS GAME
	let result = collectionArr.map((game) => new Game(game));

	//GENERATE THE MARKUP FOR EACH GAME
	for (let game of result) {
		let gameHTML = await generateCardHTML(game);
		$('#result_search').append(gameHTML);
	}

	//IF THE USER IS LOGGED IN, ADDS A CLASS TO THE 'FAVORITE BUTTON' THIS CLASS HAS AN EVENT LISTENER THAT REMOVES THE GAME CARD FROM THE SCREEN WITH THE USER DECIDES TO REMOVE THE GAME FROM THE COLLECTION LIST.
	if (id === user_logged) {
		$('.addFav').addClass('fav');
	}
}

// THIS FUNCTION IS JUST TO FIX SOME CSS FOR THE REVIEWS
async function getReviews() {
	$('body').css('background-image', `url(/static/review_background.jpg)`);
	$('body').css('background-size', `100% 100%`);
	$('#result_search').css('grid-template-columns', 'repeat(auto-fill, minmax(550px, 1fr))');
}

//CLASS THAT ORGANIZES EACH GAME AFTER RETRIEVED FROM THE API.
class Game {
	constructor(gameObj) {
		this.name = gameObj.name;
		this.released = gameObj.released;
		this.image = gameObj.background_image;
		this.metacritic = gameObj.metacritic;
		this.platforms = [];
		this.slug = gameObj.slug;
		this.genres = gameObj.genres;
		for (let platform of gameObj.platforms) {
			this.platforms.push(platform.platform.name);
		}
	}
}

// -------------------------EVENT LISTENERS ------------------------------

// THIS FUNCTION IS A INFINITE SCROLL THAT USES THE NEXTPAGE DATA TO MAKE AN API CALL WHENEVER THE USER SCROLLS TO THE END OF THE PAGE.
$('#main_content').scroll(async function() {
	if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
		let response = await axios.get(`${nextPage}`);
		let gameArr = response.data.results;
		nextPage = response.data.next;
		let result = gameArr.map((game) => new Game(game));

		for (let game of result) {
			let gameHTML = generateCardHTML(game);
			$('#result_search').append(gameHTML);
		}
	}
});

// THIS IS JUST TO PREVENT THE USER FROM SUBMITING THE FORMS BY MISTAKE BY PRESSING ENTER TO CHANGE FROM ONE FORM INPUT TO ANOTHER
$(document).on('keypress', '#add_form', function(e) {
	if (e.which == 13) {
		e.preventDefault();
	}
});

// THIS EVENT LISTENER GETS THE ATTR 'REVIEW ID' FROM A REVIEW AND MAKES AN API REQUEST TO DELETE IT. ON THE BACKEND THERE IS A CHECK TO SEE IF THE
// LOGGED USER IS THE SAME AS THE CREATOR OF THE REVIEW.
// THE MARKUP FOR REVIEWS ARE SET IN A WAY THAT THE DELETE BUTTON WOULD ONLY APPEAR FOR THE REVIEW'S CREATOR.
$(document).on('click', '.delete-button', async function(evt) {
	evt.preventDefault();

	let reviewId = $(this).attr('data-review-id');
	console.log(reviewId);

	await axios.delete(`/api/review/${reviewId}`);

	$(this).parent().parent().remove();
});

// ADD/REMOVE FAVORITE. CHANGES THE BUTTON FROM ADD TO REMOVE WHEN CLICKED. ALSO SENDS A POST OR A DELETE REQUEST BASED ON THE BUTTON THERE IS BEING SHOWN.
$(document).on('click', '#favorite', async function() {
	let inner = $(this)[0].innerText;
	let slug = $(this).attr('data-game-slug');
	if (inner === '+') {
		let addFav = await axios.post(`/api/favorite`, {
			slug
		});

		$(this).text('X');
		$(this).removeClass('btn-success');
		$(this).addClass('btn-danger');
	} else if (inner === 'X') {
		let addFav = await axios.delete(`/api/favorite/${slug}`);
		$(this).text('+');
		$(this).removeClass('btn-danger');
		$(this).addClass('btn-success');
	}
});

//BUTTONS WITH THIS CLASS WILL ONLY SHOW UP WHEN THE USER IS LOGGED IN AND CHECKING HIS/HERS OWN COLLECTION PAGE. IT REMOVES THE GAME CARD FROM THE HTML IF THE USER DECIDES TO REMOVE THE GAME FROM THE COLLECTION LIST.
$(document).on('click', '.fav', function() {
	$(this).parent().parent().parent().remove();
});

// MEDIA QUERY FOR MENU - MADE HERE INSTEAD OF ON THE CSS FILE JUST TO SHOW THAT IT CAN BE DONE. IT HIDES ONE MENU AND SHOWS ANOTHER DEPENDING ON TH WINDOW SIZE

function mediaQuery(x) {
	if (x.matches) {
		// If media query matches
		$('#lateral_menu').css('display', 'none');
		$('#main_content').css('width', '100vw');
		$('#dropdownMenuButton').css('display', 'inline-block');
		$('.navbar').css('justify-content', 'inherit');
		$('.review_card').css('width', '90%');
	} else {
		$('#main_content').css('width', '85vw');
		$('#lateral_menu').css('display', 'block');
		$('#dropdownMenuButton').css('display', 'none');
		$('.navbar').css('justify-content', 'space-between');
		$('.review_card').css('width', '50%');
	}
}

var x = window.matchMedia('(max-width: 700px)');
mediaQuery(x); // Call listener function at run time
x.addEventListener('change', mediaQuery); // Attach listener function on state changes
