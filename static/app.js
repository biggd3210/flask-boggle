// initialize variables to call event handlers

const answers = []
const submitGuess = document.getElementById("submit-guess");


async function check_word() {
    const word_val = document.getElementById('guess').value
    if (word_val) {
    const response = await axios.post("http://127.0.0.1:5000/check-word", {"word": word_val});
    const msg = response.data;
    return msg
    } else {
        alert("Please enter a word")
    }
}

async function log_game() {
    const score = document.getElementById("score").innerText;
    const response = await axios.post("http://127.0.0.1:5000/log-stats", {"score": score})
    console.log("score is ", score)
    console.log(response)
    if (response.data.brokeRecord) {
        const newHighScore = document.createElement('h2');
        newHighScore.innerText = `You broke the record highcore with new score: ${score}!`
        const title = document.getElementById("title")
        title.append(newHighScore);
    }
}

async function display_message(msg){
    let userMsg = '';
    const msg_container = document.createElement('h4');
    msg_container.setAttribute('id', 'msg-container');

    //route logic to indicate proper message.
    //add class to style css (change color per message)
    if (msg.result == 'not-on-board') {
        msg_container.setAttribute('class', 'not-on-board');
        userMsg = "That word is not on the board!"
    } else if (msg.result == 'not-word') {
        msg_container.setAttribute('class', 'not-valid');
        userMsg = "That is not a valid word!"
    } else if (msg.result == 'ok') {
        if (answers.includes(msg.word)) {
            msg_container.setAttribute('class', 'previous-answer');
            userMsg = "You've alreayd guess this word! Try again!";
        } else {
            answers.push(msg.word)
            msg_container.setAttribute('class', 'ok');
            userMsg = "Good catch! That is a valid word on the board!";
            addScore(msg.word.length);
        }
    } 
    
    msg_container.innerText = userMsg;
    document.body.append(msg_container);
}

submitGuess.addEventListener('submit', async function(evt) {
    evt.preventDefault();
    const msg = await check_word()
    await display_message(msg);
    document.getElementById('guess').value = '';
    setTimeout(function() {
        document.getElementById('msg-container').remove();
    }, 3000)
})

function addScore(word) {
    let score = document.getElementById('score');
    let scoreboard = document.getElementById('scoreboard');     

    if (score.innerText == 0) {
        scoreboard.setAttribute('style', 'visibility: visible');
        score.innerText = word;
    } else {
        const currentScore = parseInt(score.innerText);
        score.innerText = currentScore + word;
    }
}

async function endGame() {
    const submitForm = document.getElementById("submit-guess");
    const restartForm = document.getElementById("restart-game");
    submitForm.setAttribute("style", "visibility: hidden");
    restartForm.setAttribute("style", "visibility: visible");
    answer = [];

    await log_game()
}


function buildTimerStartGame() {
    
    let timer;
    let count = 60;
    let scoreboard = document.getElementById('scoreboard');
    scoreboard.setAttribute('style', 'visibility: visible')
    $('#timer-el').text(count);

    timer = setTimeout(countdown, 1000);
    
    function countdown() {
        if (count > 0) {
            count --;
            $('#timer-el').text(count);
            timer = setTimeout(countdown, 1000);
        } else {
            endGame()
        }
    }
    

}

submitGuess.addEventListener('submit', buildTimerStartGame, { once: true})