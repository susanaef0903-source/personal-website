// ============================================
// Rock, Paper, Scissors — first to 5 wins
// ============================================

// Each choice knows which choice it beats — that one line replaces
// a whole table of if/else comparisons
const BEATS = {
  rock: 'scissors',
  paper: 'rock',
  scissors: 'paper',
};

const EMOJI = {
  rock: '✊',
  paper: '✋',
  scissors: '✌️',
};

const WINNING_SCORE = 5;

const playerScoreOutput = document.getElementById('player-score');
const computerScoreOutput = document.getElementById('computer-score');
const playerHandOutput = document.getElementById('player-hand');
const computerHandOutput = document.getElementById('computer-hand');
const resultOutput = document.getElementById('result');
const choiceButtons = document.querySelectorAll('.choice-btn');
const playAgainButton = document.getElementById('play-again-btn');

let playerScore = 0;
let computerScore = 0;

// Pick rock, paper, or scissors at random for the computer
function computerPick() {
  const options = Object.keys(BEATS);
  const randomIndex = Math.floor(Math.random() * options.length);
  return options[randomIndex];
}

function playRound(playerChoice) {
  const computerChoice = computerPick();

  // Show both hands
  playerHandOutput.textContent = EMOJI[playerChoice];
  computerHandOutput.textContent = EMOJI[computerChoice];

  // Decide the round
  resultOutput.classList.remove('win', 'lose');
  if (playerChoice === computerChoice) {
    resultOutput.textContent = "It's a tie!";
  } else if (BEATS[playerChoice] === computerChoice) {
    playerScore++;
    resultOutput.textContent = `${capitalize(playerChoice)} beats ${computerChoice} — you win this round!`;
    resultOutput.classList.add('win');
  } else {
    computerScore++;
    resultOutput.textContent = `${capitalize(computerChoice)} beats ${playerChoice} — computer wins this round.`;
    resultOutput.classList.add('lose');
  }

  playerScoreOutput.textContent = playerScore;
  computerScoreOutput.textContent = computerScore;

  // Has anyone won the whole match?
  if (playerScore === WINNING_SCORE || computerScore === WINNING_SCORE) {
    endMatch();
  }
}

function endMatch() {
  if (playerScore === WINNING_SCORE) {
    resultOutput.textContent = '🎉 You won the match!';
    resultOutput.classList.add('win');
  } else {
    resultOutput.textContent = 'The computer won the match. Rematch?';
    resultOutput.classList.add('lose');
  }

  // Freeze the choice buttons until the player starts a new match
  choiceButtons.forEach((button) => (button.disabled = true));
  playAgainButton.classList.remove('hidden');
}

function resetMatch() {
  playerScore = 0;
  computerScore = 0;
  playerScoreOutput.textContent = '0';
  computerScoreOutput.textContent = '0';
  playerHandOutput.textContent = '❔';
  computerHandOutput.textContent = '❔';
  resultOutput.textContent = 'Make your first move!';
  resultOutput.classList.remove('win', 'lose');

  choiceButtons.forEach((button) => (button.disabled = false));
  playAgainButton.classList.add('hidden');
}

function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

// Wire up the buttons
choiceButtons.forEach((button) => {
  button.addEventListener('click', () => playRound(button.dataset.choice));
});

playAgainButton.addEventListener('click', resetMatch);
