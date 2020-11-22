// SOME VARIABLES NEED TO BE HARD CODED DUE TO THE API SCHEMA.

const BASE_URL = 'https://api.rawg.io/api';

// EACH API REQUEST SEND A LINK FOR THE 'NEXT PAGE' RESULTS. I ADDED A EMPTY VARIABLE SO I CAN USE THE DATA GLOBALLY
let nextPage = '';

// GETTING DATES FOR THE FIRST SEARCH - TRENDING ON THE LAST YEAR

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

//THIS USES THE TITLE OF THE PAGE TO KNOW WHAT NEEDS TO BE SEARCHED. IT CALLS mainSearch TO GET THE GAMES
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
		let gameHTML = generateCardHTML(game);
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

//THIS USES THE TITLE OF THE PAGE TO KNOW WHAT NEEDS TO BE SEARCHED. IT CALLS getDataPlat TO GET THE GAMES
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
		let gameHTML = generateCardHTML(game);
		$('#result_search').append(gameHTML);
	}
}

//CREATES THE MARKUP FOR EACH GAME CARD

function generateCardHTML(game) {
	let gameName = game.name;
	let gameRel = game.released;
	let gameImg = game.image;
	let metacritic = game.metacritic;
	let platforms = game.platforms;
	let slug = game.slug;
	let genres = game.genres;

	if (metacritic === null) {
		metacritic = 'NA';
	}

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

	let markupList = '';

	for (g of genres) {
		if (g.name === 'Massively Multiplayer') {
			g.name = 'MMO';
		}
		let genreSlug = g.name.toLowerCase();

		let genre_markup = `<a href='/genres/${genreSlug}' class='genre'><span class='card-data mr-1'>${g.name}</span></a>`;
		markupList = markupList + genre_markup;
	}

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

							
							<button class='btn btn-dark' id='add-review'>ADD REVIEW</button><button class='btn btn-dark' id='favorite'>ADD FAVORITE</button>
                            

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

// THIS FUNCTION REMOVE SOME DIVS FROM THE HTML, ADDS A NEW BACKGROUND, GETS THE REVIEWS FROM THE DATABASE AND ADD THEM TO THE HTML

async function getReviews() {
	$('body').css('background-image', `url(/static/review_background.jpg)`);
	$('body').css('background-size', `100% 100%`);
	$('#result_search').remove();
	$('#main_content').append(`<div id='reviews'></div>`);
	$('#result_search').css('grid-template-columns', 'repeat(auto-fill, minmax(550px, 1fr))');
	const resp = await axios.get(`http://127.0.0.1:5000/api/reviews`);
	for (review of resp.data.reviews) {
		let reviewMarkup = `
	
	<div class='review_card'>
		<div class='review_title'>${review.title}</div>
		<div class='review_game'><a href='/games/${review.game_slug}'>${review.game_name}</a></div>
		
		<div class='review_text'>${review.review}</div>
		<div class='review_user'><small>Created by: ${review.username}</small></div>
	</div>
		
	`;

		$('#reviews').append(reviewMarkup);
	}
}

$(document).on('keypress', '#add_form', function(e) {
	if (e.which == 13) {
		e.preventDefault();
	}
});

// MEDIA QUERY FOR MENU - MADE HERE INSTEAD OF ON THE CSS FILE JUST TO SHOW THAT IT CAN BE DONE. IT HIDES ONE MENU AND SHOWS ANOTHER DEPENDING ON TH WINDOW SIZE

function mediaQuery(x) {
	if (x.matches) {
		// If media query matches
		$('#lateral_menu').css('display', 'none');
		$('#main_content').css('width', '100vw');
		$('#dropdownMenuButton').css('display', 'inline-block');
		$('.navbar').css('justify-content', 'inherit');
	} else {
		$('#main_content').css('width', '85vw');
		$('#lateral_menu').css('display', 'block');
		$('#dropdownMenuButton').css('display', 'none');
		$('.navbar').css('justify-content', 'space-between');
	}
}

var x = window.matchMedia('(max-width: 700px)');
mediaQuery(x); // Call listener function at run time
x.addEventListener('change', mediaQuery); // Attach listener function on state changes
