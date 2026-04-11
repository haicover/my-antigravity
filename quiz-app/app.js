// State
let currentQuestionIndex = 0;
let score = 0;
let timeLeft = 60;
let timerId = null;
let isAnswered = false;
let userAnswers = []; // To store user answer path

// DOM Elements
const screens = {
  start: document.getElementById('startScreen'),
  quiz: document.getElementById('quizScreen'),
  result: document.getElementById('resultScreen'),
  review: document.getElementById('reviewScreen')
};

const btnStart = document.getElementById('btnStart');
const btnPlayAgain = document.getElementById('btnPlayAgain');
const btnReview = document.getElementById('btnReview');
const btnBackToResult = document.getElementById('btnBackToResult');

const questionCountDisplay = document.getElementById('questionCount');
const scoreDisplay = document.getElementById('scoreDisplay');
const timerBar = document.getElementById('timerBar');
const timerText = document.getElementById('timerText');
const questionText = document.getElementById('questionText');
const optionsContainer = document.getElementById('optionsContainer');

const scoreRing = document.getElementById('scoreRing');
const finalScore = document.getElementById('finalScore');
const resultMessage = document.getElementById('resultMessage');

const reviewContainer = document.getElementById('reviewContainer');

// Event Listeners
btnStart.addEventListener('click', startQuiz);
btnPlayAgain.addEventListener('click', resetQuiz);
btnReview.addEventListener('click', showReviewScreen);
btnBackToResult.addEventListener('click', () => showScreen('result'));

// Functions
function showScreen(screenKey) {
  Object.values(screens).forEach(screen => screen.classList.remove('active'));
  screens[screenKey].classList.add('active');
}

function startQuiz() {
  score = 0;
  currentQuestionIndex = 0;
  userAnswers = [];
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
  
  userAnswers.push({
    questionIndex: currentQuestionIndex,
    selectedIndex: null,
    isCorrect: false,
    timedOut: true
  });
  
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
  
  userAnswers.push({
    questionIndex: currentQuestionIndex,
    selectedIndex: selectedIndex,
    isCorrect: selectedIndex === correctIndex,
    timedOut: false
  });
  
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

function showReviewScreen() {
  showScreen('review');
  reviewContainer.innerHTML = '';
  
  userAnswers.forEach(answerObj => {
    const qData = quizQuestions[answerObj.questionIndex];
    
    const item = document.createElement('div');
    item.className = 'review-item';
    
    // Check if it was a timeout
    let selectionStateText = '';
    if (answerObj.timedOut) {
      selectionStateText = '<span style="color:var(--incorrect); font-size: 0.85rem; margin-bottom: 8px; display:inline-block">⏱ Time Out (-1 pt)</span>';
    }
    
    item.innerHTML = `
      ${selectionStateText}
      <h3 class="review-question">${answerObj.questionIndex + 1}. ${qData.question}</h3>
      <div class="review-options">
        ${qData.options.map((opt, i) => {
          let cssClass = 'review-option';
          let icon = '';
          
          if (i === qData.answer) {
             cssClass += ' correct';
             icon = '<span class="review-option-icon">✓</span>';
          } else if (i === answerObj.selectedIndex) {
             cssClass += ' incorrect';
             icon = '<span class="review-option-icon">✗</span>';
          }
          
          return `<div class="${cssClass}">
            <span>${opt}</span>
            ${icon}
          </div>`;
        }).join('')}
      </div>
    `;
    reviewContainer.appendChild(item);
  });
}
