const genre = [ 'action', 'strategy', 'rpg', 'shooter', 'adventure', 'puzzle', 'racing', 'sports' ];

const BASE_URL = 'https://api.rawg.io/api';

let nextPage = '';

// GETTING DATES

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = yyyy + '-' + mm + '-' + dd;

yyyy = String(parseInt(yyyy) - 1);
next = yyyy + '-' + mm + '-' + dd;

const startSearchUrl = `https://api.rawg.io/api/games?dates=${next},${today}&-ratings`;

let platList = [];

let platIDList = [];

const playstation = '<i class="fab fa-playstation"></i>';
const pc = '<i class="fas fa-desktop"></i>';
const xbox = '<i class="fab fa-xbox"></i>';
const nSwitch = '<i class="fab fa-neos"></i>';
const android = '<i class="fab fa-android"></i>';
const ios = '<i class="fab fa-apple"></i>';

let platIcon = [ pc, playstation, xbox, nSwitch, android, ios ];

// ------------------------------------------------

async function getGenre() {
	$('#result_search').empty();

	let target = $('#title');
	let genreName = target.text().toLowerCase();

	if (genreName === 'rpg') {
		genreName = 'role-playing-games-rpg';
	}

	await getDataGenre(genreName);
}

async function searchBox() {
	$('#result_search').empty();

	let target = $('#title');
	let searchText = target.text().toLowerCase();

	await mainSearch(searchText);
}

async function getPlatform() {
	$('#result_search').empty();

	let target = $('#title');
	let platName = target.text().toLowerCase();

	await getDataPlat(platName);
}

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

async function getPlatInfo() {
	// 	GET LIST OF PLATFORM IDS TO BE USED LATER TO GET THE GAMES

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

// ------------INFINITE SCROLL---------------

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

// -------------MEDIA QUERY FOR MENU ---------------

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
