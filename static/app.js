const genre = [ 'action', 'strategy', 'rpg', 'shooter', 'adventure', 'puzzle', 'racing', 'sports' ];

const BASE_URL = 'https://api.rawg.io/api';

let nextPage = '';

const startSearchUrl = 'https://api.rawg.io/api/games?dates=2020-01-01,2020-11-01&-ratings';

let platList = [];

let platIDList = [];

const playstation = '<i class="fab fa-playstation"></i>';
const pc = '<i class="fas fa-desktop"></i>';
const xbox = '<i class="fab fa-xbox"></i>';
const nSwitch = '<i class="fab fa-neos"></i>';
const android = '<i class="fab fa-android"></i>';
const ios = '<i class="fab fa-apple"></i>';

let platIcon = [ pc, playstation, xbox, nSwitch, android, ios ];

getPlatInfo();

// ------------------------------------------------

$('.genre').on('click', async function(evt) {
	$('#result_search').empty();
	evt.preventDefault();
	let target = evt.target;
	let genreName = target.innerText.toLowerCase();
	$('#title').text(genreName.toUpperCase());

	if (genreName === 'rpg') {
		genreName = 'role-playing-games-rpg';
	}

	await getDataGenre(genreName);
});

$('#search_box').on('submit', async function(evt) {
	$('#result_search').empty();
	evt.preventDefault();
	let target = evt.target;

	await mainSearch();
	let searchText = $('.form-control').val().toUpperCase();
	$('#title').text(`Results for: ${searchText}`);
});

$('.platform').on('click', async function(evt) {
	$('#result_search').empty();
	evt.preventDefault();
	let target = evt.target;
	let platName = target.innerText.toLowerCase();
	$('#title').text(platName.toUpperCase());

	await getDataPlat(platName);
});

async function getDataPlat(platName) {
	let platID = '';

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

	const gameMarkup = $(`
    
    
        <div class="col card_search">
            
                    <div class="card">
                        <img class="card-img-top" src="${gameImg}" alt="Card image cap">
                        <div class="card-body">
                            <div class='container-fluid icons'>
                               ${icon}
                                <i class='btn btn-success p-1 score '>${metacritic}</i>
                            </div> 
                            <h5 class="card-title">${gameName}</h5> 

                            <br>
                            <br>

                            <ul class=" list-group-flush card_list">
                                <li class="list-group-item">Release Date:<span class='card-data'>${gameRel}</span></li>
                                <li class="list-group-item">Genre:</li>
                                <li class="list-group-item">Chart:</li>
                                <br>
                                <li class="list-group-item text-center">STREAMING</li>
                            </ul>
                        </div>
                    </div>
                    
        </div>
    
    `);

	return gameMarkup;
}

async function mainSearch() {
	let $searchData = $('.form-control').val();
	let response = await axios.get(`${BASE_URL}/games?search='${$searchData}'`);
	let gameArr = response.data.results;
	nextPage = response.data.next;
	let result = gameArr.map((game) => new Game(game));

	for (let game of result) {
		let gameHTML = generateCardHTML(game);
		$('#result_search').append(gameHTML);
	}
}

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

class Game {
	constructor(gameObj) {
		this.name = gameObj.name;
		this.released = gameObj.released;
		this.image = gameObj.background_image;
		this.metacritic = gameObj.metacritic;
		this.platforms = [];
		for (let platform of gameObj.platforms) {
			this.platforms.push(platform.platform.name);
		}
	}
}

startSearch();

// --------------------------------

$('#main_content').scroll(async function() {
	if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
		console.log('Bottom Reached');
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
