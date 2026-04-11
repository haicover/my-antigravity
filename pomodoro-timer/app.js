const DOM = {
  timeDisplay: document.getElementById('time'),
  statusText: document.getElementById('statusText'),
  sessionCount: document.getElementById('sessionCount'),
  btnPlayPause: document.getElementById('btnPlayPause'),
  btnPlayPauseText: document.getElementById('btnPlayPauseText'),
  iconPlay: document.querySelector('.icon-play'),
  iconPause: document.querySelector('.icon-pause'),
  btnReset: document.getElementById('btnReset'),
  tabs: document.querySelectorAll('.mode-tab'),
  progressCircle: document.querySelector('.progress-ring__circle'),
  audio: document.getElementById('alarmSound'),
  // Settings
  btnThemeToggle: document.getElementById('btnThemeToggle'),
  iconSun: document.querySelector('.icon-sun'),
  iconMoon: document.querySelector('.icon-moon'),
  soundToggle: document.getElementById('soundToggle'),
  btnSettings: document.getElementById('btnSettings'),
  btnCloseSettings: document.getElementById('btnCloseSettings'),
  btnSaveSettings: document.getElementById('btnSaveSettings'),
  settingsModal: document.getElementById('settingsModal'),
  inputs: {
    work: document.getElementById('workTime'),
    shortBreak: document.getElementById('shortBreakTime'),
    longBreak: document.getElementById('longBreakTime'),
    longBreakInterval: document.getElementById('longBreakInterval')
  }
};

const MODES = {
  work: { id: 'work', label: 'Focus Time', colorVar: '--work' },
  shortBreak: { id: 'shortBreak', label: 'Short Break', colorVar: '--short' },
  longBreak: { id: 'longBreak', label: 'Long Break', colorVar: '--long' }
};

// SVG Circle properties
const CIRCLE_RADIUS = 140;
const CIRCUMFERENCE = 2 * Math.PI * CIRCLE_RADIUS;
DOM.progressCircle.style.strokeDasharray = `${CIRCUMFERENCE} ${CIRCUMFERENCE}`;
DOM.progressCircle.style.strokeDashoffset = CIRCUMFERENCE;

// State
let intervals = { work: 25, shortBreak: 5, longBreak: 15 };
let longBreakInterval = 4;
let completedSessions = 0;
let soundEnabled = true;
let currentTheme = 'dark';

let currentMode = 'work';
let timeLeft = intervals[currentMode] * 60;
let timerId = null;
let isRunning = false;

// Initialization
function init() {
  loadSettings();
  updateUI();
  setupEventListeners();
}

// Timer Logic
function startTimer() {
  if (isRunning) return;
  isRunning = true;
  timerId = setInterval(() => {
    if (timeLeft > 0) {
      timeLeft--;
      updateUI();
    } else {
      handleSessionEnd();
    }
  }, 1000);
  
  DOM.iconPlay.classList.add('hidden');
  DOM.iconPause.classList.remove('hidden');
  DOM.btnPlayPauseText.textContent = 'Pause';
}

function pauseTimer() {
  if (!isRunning) return;
  isRunning = false;
  clearInterval(timerId);
  
  DOM.iconPlay.classList.remove('hidden');
  DOM.iconPause.classList.add('hidden');
  DOM.btnPlayPauseText.textContent = 'Resume';
}

function resetTimer() {
  pauseTimer();
  timeLeft = intervals[currentMode] * 60;
  updateUI(true);
}

function switchMode(modeId) {
  pauseTimer();
  currentMode = modeId;
  timeLeft = intervals[currentMode] * 60;
  
  // Update Tabs UI
  DOM.tabs.forEach(tab => {
    tab.classList.toggle('active', tab.dataset.mode === modeId);
  });

  // Update styling
  const color = MODES[modeId].colorVar;
  document.documentElement.style.setProperty('--accent', `var(${color})`);
  document.documentElement.style.setProperty('--accent-dim', `color-mix(in srgb, var(${color}) 15%, transparent)`);
  
  DOM.statusText.textContent = MODES[modeId].label;
  
  updateUI(true); // reset progress explicitly when switching
}

function handleSessionEnd() {
  pauseTimer();
  
  // Play sound
  if (soundEnabled) {
    DOM.audio.currentTime = 0;
    DOM.audio.play().catch(e => console.log('Audio play failed', e));
  }

  if (currentMode === 'work') {
    completedSessions++;
    updateStatsUI();
    if (completedSessions % longBreakInterval === 0) {
      switchMode('longBreak');
    } else {
      switchMode('shortBreak');
    }
  } else {
    // If break ends, go back to work
    switchMode('work');
  }
}

// UI Updates
function updateUI(resetProgress = false) {
  // Time formatting
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const timeStr = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  
  DOM.timeDisplay.textContent = timeStr;
  document.title = `${timeStr} - ${MODES[currentMode].label}`;

  // Progress Circle
  const totalTime = intervals[currentMode] * 60;
  let progress = totalTime > 0 ? (totalTime - timeLeft) / totalTime : 0;
  
  // Force reset transition when explicitly changing modes
  if (resetProgress || timeLeft === totalTime) {
    DOM.progressCircle.style.transition = 'none';
    DOM.progressCircle.style.strokeDashoffset = CIRCUMFERENCE;
    // Trigger reflow
    DOM.progressCircle.getBoundingClientRect();
    DOM.progressCircle.style.transition = 'stroke-dashoffset 0.1s linear, stroke 0.5s ease';
  } else {
    const offset = CIRCUMFERENCE - (progress * CIRCUMFERENCE);
    DOM.progressCircle.style.strokeDashoffset = offset;
  }
}

function updateStatsUI() {
  DOM.sessionCount.textContent = `${completedSessions % longBreakInterval} / ${longBreakInterval}`;
  // Optionally display total absolute completed pomodoros: `${completedSessions}`
}

// Settings
function loadSettings() {
  const saved = localStorage.getItem('pomoSettings');
  if (saved) {
    const parsed = JSON.parse(saved);
    intervals = parsed.intervals || intervals;
    longBreakInterval = parsed.longBreakInterval || longBreakInterval;
    soundEnabled = parsed.soundEnabled !== undefined ? parsed.soundEnabled : true;
    currentTheme = parsed.theme || 'dark';
  }
  
  // Apply theme
  applyTheme(currentTheme);
  
  // Sync inputs
  DOM.inputs.work.value = intervals.work;
  DOM.inputs.shortBreak.value = intervals.shortBreak;
  DOM.inputs.longBreak.value = intervals.longBreak;
  DOM.inputs.longBreakInterval.value = longBreakInterval;
  DOM.soundToggle.checked = soundEnabled;

  updateStatsUI();
  resetTimer();
}

function applyTheme(theme) {
  document.body.dataset.theme = theme;
  if(theme === 'light') {
    DOM.iconSun.classList.add('hidden');
    DOM.iconMoon.classList.remove('hidden');
  } else {
    DOM.iconSun.classList.remove('hidden');
    DOM.iconMoon.classList.add('hidden');
  }
}

function toggleTheme() {
  currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
  applyTheme(currentTheme);
  saveSettings(false); // background save
}

function saveSettings(restartTimer = true) {
  intervals.work = parseInt(DOM.inputs.work.value) || 25;
  intervals.shortBreak = parseInt(DOM.inputs.shortBreak.value) || 5;
  intervals.longBreak = parseInt(DOM.inputs.longBreak.value) || 15;
  longBreakInterval = parseInt(DOM.inputs.longBreakInterval.value) || 4;
  soundEnabled = DOM.soundToggle.checked;

  localStorage.setItem('pomoSettings', JSON.stringify({
    intervals,
    longBreakInterval,
    soundEnabled,
    theme: currentTheme
  }));

  updateStatsUI();
  if (restartTimer) {
    switchMode(currentMode); // Reset current timer with new setting
  }
  toggleModal(false);
}

function toggleModal(show) {
  if (show) {
    DOM.settingsModal.classList.add('active');
  } else {
    DOM.settingsModal.classList.remove('active');
  }
}

// Listeners
function setupEventListeners() {
  DOM.btnPlayPause.addEventListener('click', () => {
    isRunning ? pauseTimer() : startTimer();
  });

  DOM.btnReset.addEventListener('click', resetTimer);

  DOM.tabs.forEach(tab => {
    tab.addEventListener('click', (e) => switchMode(e.target.dataset.mode));
  });

  DOM.btnThemeToggle.addEventListener('click', toggleTheme);
  DOM.btnSettings.addEventListener('click', () => toggleModal(true));
  DOM.btnCloseSettings.addEventListener('click', () => toggleModal(false));
  DOM.btnSaveSettings.addEventListener('click', () => saveSettings(true));
  
  DOM.settingsModal.addEventListener('click', (e) => {
    if (e.target === DOM.settingsModal) toggleModal(false);
  });
}

// Boot
init();
