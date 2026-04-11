// State
let currentQuestionIndex = 0;
let score = 0;
let timeLeft = 60;
let timerId = null;
let isAnswered = false;

// DOM Elements
const screens = {
  start: document.getElementById('startScreen'),
  quiz: document.getElementById('quizScreen'),
  result: document.getElementById('resultScreen')
};

const btnStart = document.getElementById('btnStart');
const btnPlayAgain = document.getElementById('btnPlayAgain');

const questionCountDisplay = document.getElementById('questionCount');
const scoreDisplay = document.getElementById('scoreDisplay');
const timerBar = document.getElementById('timerBar');
const timerText = document.getElementById('timerText');
const questionText = document.getElementById('questionText');
const optionsContainer = document.getElementById('optionsContainer');

const scoreRing = document.getElementById('scoreRing');
const finalScore = document.getElementById('finalScore');
const resultMessage = document.getElementById('resultMessage');

// Event Listeners
btnStart.addEventListener('click', startQuiz);
btnPlayAgain.addEventListener('click', resetQuiz);

// Functions
function showScreen(screenKey) {
  Object.values(screens).forEach(screen => screen.classList.remove('active'));
  screens[screenKey].classList.add('active');
}

function startQuiz() {
  score = 0;
  currentQuestionIndex = 0;
  showScreen('quiz');
  loadQuestion();
}

function loadQuestion() {
  isAnswered = false;
  const currentQ = quizQuestions[currentQuestionIndex];
  
  // Update UI Stats
  questionCountDisplay.textContent = `${currentQuestionIndex + 1} / ${quizQuestions.length}`;
  scoreDisplay.textContent = score;
  
  // Set text
  questionText.textContent = currentQ.question;
  
  // Generate options
  optionsContainer.innerHTML = '';
  currentQ.options.forEach((optionText, index) => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.textContent = optionText;
    btn.onclick = () => selectAnswer(index, btn);
    optionsContainer.appendChild(btn);
  });
  
  startTimer();
}

function startTimer() {
  clearInterval(timerId);
  timeLeft = 60;
  updateTimerUI();
  
  timerId = setInterval(() => {
    timeLeft--;
    updateTimerUI();
    
    if (timeLeft <= 0) {
      clearInterval(timerId);
      handleTimeout();
    }
  }, 1000);
}

function updateTimerUI() {
  timerText.textContent = `${timeLeft}s`;
  const percentage = (timeLeft / 60) * 100;
  timerBar.style.setProperty('--progress', `${percentage}%`);
  
  // change color if time is low
  if (percentage <= 20) {
    timerText.style.color = 'var(--incorrect)';
  } else {
    timerText.style.color = 'var(--text-muted)';
  }
}

function handleTimeout() {
  if (isAnswered) return;
  isAnswered = true;
  score--; // Decrement score on timeout per requirement
  scoreDisplay.textContent = score;
  
  // Highlight correct answer
  const correctIndex = quizQuestions[currentQuestionIndex].answer;
  const buttons = optionsContainer.querySelectorAll('.option-btn');
  buttons[correctIndex].classList.add('correct');
  
  disableAllOptions();
  
  // Wait then go next
  setTimeout(nextQuestion, 2000);
}

function selectAnswer(selectedIndex, selectedBtn) {
  if (isAnswered) return;
  isAnswered = true;
  clearInterval(timerId);
  
  const correctIndex = quizQuestions[currentQuestionIndex].answer;
  const buttons = optionsContainer.querySelectorAll('.option-btn');
  
  disableAllOptions();
  
  if (selectedIndex === correctIndex) {
    selectedBtn.classList.add('correct');
    score++;
  } else {
    selectedBtn.classList.add('incorrect');
    buttons[correctIndex].classList.add('correct');
  }
  
  scoreDisplay.textContent = score;
  
  setTimeout(nextQuestion, 1500);
}

function disableAllOptions() {
  const buttons = optionsContainer.querySelectorAll('.option-btn');
  buttons.forEach(btn => btn.disabled = true);
}

function nextQuestion() {
  currentQuestionIndex++;
  if (currentQuestionIndex < quizQuestions.length) {
    loadQuestion();
  } else {
    endQuiz();
  }
}

function endQuiz() {
  showScreen('result');
  finalScore.textContent = score;
  
  const maxScore = quizQuestions.length;
  // If user timed out a lot, score can be negative. Cap lower bound at 0 for UI progress scaling
  const displayScore = Math.max(0, score);
  const percentage = displayScore / maxScore;
  
  // Animate SVG Ring (Circumference is 440 = 2 * PI * 70)
  const offset = 440 - (percentage * 440);
  
  // Needs a small delay for CSS transition to trigger after display:flex block loads
  setTimeout(() => {
    scoreRing.style.strokeDashoffset = offset;
  }, 100);
  
  if (percentage >= 0.8) {
    resultMessage.textContent = "Outstanding! You possess true Elite knowledge.";
    scoreRing.style.stroke = "var(--correct)";
  } else if (percentage >= 0.5) {
    resultMessage.textContent = "Good job. With a little more practice, you'll be unstoppable.";
    scoreRing.style.stroke = "var(--primary)";
  } else {
    resultMessage.textContent = "Keep learning! Every failure is a stepping stone to success.";
    scoreRing.style.stroke = "var(--incorrect)";
  }
}

function resetQuiz() {
  scoreRing.style.strokeDashoffset = 440;
  scoreRing.style.stroke = "var(--primary)";
  startQuiz();
}
