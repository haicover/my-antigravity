/* ═══════════════════════════════════════════════════════════════
   Elite Weather App Logic
   Version: 1.0 (Vibe Coding 2026)
   ═══════════════════════════════════════════════════════════════ */

// DOM Elements
const els = {
  searchInput: document.getElementById('searchInput'),
  searchSuggestions: document.getElementById('searchSuggestions'),
  locationBtn: document.getElementById('locationBtn'),
  loadingState: document.getElementById('loadingState'),
  weatherContent: document.getElementById('weatherContent'),
  
  cityName: document.getElementById('cityName'),
  currentDate: document.getElementById('currentDate'),
  currentIcon: document.getElementById('currentIcon'),
  currentTemp: document.getElementById('currentTemp'),
  weatherDesc: document.getElementById('weatherDescription'),
  tempHigh: document.getElementById('tempHigh'),
  tempLow: document.getElementById('tempLow'),
  
  humidity: document.getElementById('humidity'),
  windSpeed: document.getElementById('windSpeed'),
  rainChance: document.getElementById('rainChance'),
  uvIndex: document.getElementById('uvIndex'),
  
  hourlyForecast: document.getElementById('hourlyForecast')
};

// Weather Code Mapping (WMO) -> { theme, name, svg }
const weatherMap = {
  0: { theme: 'sunny', name: 'Clear Sky', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#f1c40f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>' },
  1: { theme: 'sunny', name: 'Mainly Clear', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#f1c40f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 8.5V9m0 0v.5m0-.5h.5m-.5 0h-.5M2 13.5A3.5 3.5 0 0 1 5.5 10a3.5 3.5 0 0 1 3.5 3.5M2 13.5h7m-7 0A3.5 3.5 0 0 0 5.5 17a3.5 3.5 0 0 0 3.5-3.5M9 13.5v-1a5 5 0 0 1 10 0v1m-10 0h10m-10 0A5 5 0 0 0 14 18.5a5 5 0 0 0 5-5"></path></svg>' },
  2: { theme: 'cloudy', name: 'Partly Cloudy', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#bdc3c7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-8.22c.38.05.75.12 1.11.22A5 5 0 1 1 17.5 19z"></path></svg>' },
  3: { theme: 'cloudy', name: 'Overcast', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#7f8c8d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"></path></svg>' },
  45: { theme: 'cloudy', name: 'Foggy', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#95a5a6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="10" x2="20" y2="10"></line><line x1="4" y1="14" x2="20" y2="14"></line><line x1="8" y1="18" x2="16" y2="18"></line><line x1="8" y1="6" x2="16" y2="6"></line></svg>' },
  51: { theme: 'rainy', name: 'Light Drizzle', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#3498db" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 16.2A4.5 4.5 0 0 0 17.5 8h-1.8A7 7 0 1 0 4 14.9"></path><path d="M16 14v6"></path><path d="M8 14v6"></path><path d="M12 16v6"></path></svg>' },
  61: { theme: 'rainy', name: 'Little Rain', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#2980b9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 16.2A4.5 4.5 0 0 0 17.5 8h-1.8A7 7 0 1 0 4 14.9"></path><path d="M16 14v6"></path><path d="M8 14v6"></path><path d="M12 16v6"></path></svg>' },
  63: { theme: 'rainy', name: 'Rain', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#2c3e50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 16.2A4.5 4.5 0 0 0 17.5 8h-1.8A7 7 0 1 0 4 14.9"></path><path d="M16 14v6"></path><path d="M8 14v6"></path><path d="M12 16v6"></path></svg>' },
  71: { theme: 'night', name: 'Snow', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#ecf0f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 16.2A4.5 4.5 0 0 0 17.5 8h-1.8A7 7 0 1 0 4 14.9"></path><path d="M16 14v6"></path><path d="M8 14v6"></path><path d="M12 16v6"></path></svg>' },
  95: { theme: 'night', name: 'Thunderstorm', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#f1c40f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 16.9A5 5 0 0 0 18 7h-1.26a8 8 0 1 0-11.62 9"></path><polyline points="13 11 9 17 15 17 11 23"></polyline></svg>' }
};

function getWeatherMeta(code) {
  // Approximate matching for ranges if exact code doesn't exist
  if (!weatherMap[code]) {
    if (code > 50 && code < 70) return weatherMap[61]; // Rain fallback
    if (code > 70 && code < 80) return weatherMap[71]; // Snow
    if (code > 80) return weatherMap[95]; // Thunder
    return weatherMap[2]; // Default cloudy fallback
  }
  return weatherMap[code];
}

// ─── Initialization ────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  // Try to use geolocation by default, otherwise load a default city
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => fetchWeatherByCoords(pos.coords.latitude, pos.coords.longitude, "Current Location"),
      () => fetchWeatherByCity('Hanoi')
    );
  } else {
    fetchWeatherByCity('Hanoi');
  }
});

function setupEventListeners() {
  let debounceTimer;
  els.searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    const val = e.target.value.trim();
    if (val.length < 2) {
      els.searchSuggestions.classList.add('hidden');
      return;
    }
    debounceTimer = setTimeout(() => searchCities(val), 500);
  });

  els.locationBtn.addEventListener('click', () => {
    if (navigator.geolocation) {
      setLoading(true);
      navigator.geolocation.getCurrentPosition(
        pos => fetchWeatherByCoords(pos.coords.latitude, pos.coords.longitude, "Current Location"),
        err => alert("Could not retrieve location. Please check your browser permissions.")
      );
    }
  });

  // Close suggestions when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-box') && !e.target.closest('.suggestions-dropdown')) {
      els.searchSuggestions.classList.add('hidden');
    }
  });
}

// ─── API Calls ─────────────────────────────────────────────

async function searchCities(query) {
  try {
    const res = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=5&language=en&format=json`);
    const data = await res.json();
    if (data.results) {
      renderSuggestions(data.results);
    } else {
      els.searchSuggestions.classList.add('hidden');
    }
  } catch (err) {
    console.error("Geocoding failed:", err);
  }
}

function renderSuggestions(cities) {
  els.searchSuggestions.innerHTML = '';
  cities.forEach(city => {
    const div = document.createElement('div');
    div.className = 'suggestion-item';
    const loc = city.admin1 ? `${city.name}, ${city.admin1}, ${city.country}` : `${city.name}, ${city.country}`;
    div.textContent = loc;
    div.addEventListener('click', () => {
      els.searchInput.value = city.name;
      els.searchSuggestions.classList.add('hidden');
      fetchWeatherByCoords(city.latitude, city.longitude, city.name);
    });
    els.searchSuggestions.appendChild(div);
  });
  els.searchSuggestions.classList.remove('hidden');
}

async function fetchWeatherByCity(cityName) {
  setLoading(true);
  try {
    const res = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(cityName)}&count=1&language=en&format=json`);
    const data = await res.json();
    if (data.results && data.results.length > 0) {
      fetchWeatherByCoords(data.results[0].latitude, data.results[0].longitude, data.results[0].name);
    } else {
      setLoading(false);
      alert("City not found.");
    }
  } catch (err) {
    console.error(err);
    setLoading(false);
  }
}

async function fetchWeatherByCoords(lat, lon, name) {
  setLoading(true);
  try {
    // Open-Meteo advanced endpoint
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation_probability,weather_code&hourly=temperature_2m,weather_code&daily=uv_index_max,temperature_2m_max,temperature_2m_min&timezone=auto`;
    const res = await fetch(url);
    const data = await res.json();
    
    updateUI(name, data);
  } catch (err) {
    console.error("Weather fetch failed:", err);
    alert("Could not load weather data.");
  } finally {
    setLoading(false);
  }
}

// ─── UI Updates ────────────────────────────────────────────

function setLoading(isLoading) {
  if (isLoading) {
    els.loadingState.classList.remove('hidden');
    els.weatherContent.classList.add('hidden');
  } else {
    els.loadingState.classList.add('hidden');
    els.weatherContent.classList.remove('hidden');
  }
}

function updateUI(cityName, data) {
  const current = data.current;
  const daily = data.daily;
  const hourly = data.hourly;
  
  const meta = getWeatherMeta(current.weather_code);
  
  // Theme updates
  document.body.className = `theme-${meta.theme}`;
  
  // Header
  els.cityName.textContent = cityName;
  
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  els.currentDate.textContent = new Date().toLocaleDateString('en-US', options);
  
  // Current Main
  els.currentIcon.innerHTML = meta.svg;
  els.currentTemp.textContent = Math.round(current.temperature_2m);
  els.weatherDesc.textContent = meta.name;
  
  // High/Low
  els.tempHigh.textContent = Math.round(daily.temperature_2m_max[0]);
  els.tempLow.textContent = Math.round(daily.temperature_2m_min[0]);
  
  // Details
  els.humidity.textContent = `${current.relative_humidity_2m}%`;
  els.windSpeed.textContent = `${Math.round(current.wind_speed_10m)} km/h`;
  els.rainChance.textContent = `${current.precipitation_probability}%`;
  els.uvIndex.textContent = daily.uv_index_max[0] ? daily.uv_index_max[0].toFixed(1) : '0';
  
  // 24-Hour Forecast
  renderHourly(hourly);
}

function renderHourly(hourly) {
  els.hourlyForecast.innerHTML = '';
  
  // Get current hour index
  const now = new Date();
  const currentHourISO = now.toISOString().slice(0, 14) + "00"; // roughly matching format
  
  // Find index or use 0
  let startIndex = 0;
  for(let i=0; i<hourly.time.length; i++) {
    if(new Date(hourly.time[i]).getTime() >= now.getTime()) {
      startIndex = i;
      break;
    }
  }
  
  // Show next 24 hours
  for (let i = startIndex; i < startIndex + 24; i += Math.floor(24/8)) { // Show 8 items roughly evenly spaced
     if (i >= hourly.time.length) break;
     
     const timeStr = new Date(hourly.time[i]).toLocaleTimeString('en-US', { hour: 'numeric', hour12: true });
     
     const itemMeta = getWeatherMeta(hourly.weather_code[i]);
     const temp = Math.round(hourly.temperature_2m[i]);
     
     const div = document.createElement('div');
     div.className = 'hourly-item';
     div.innerHTML = `
       <div class="hourly-time">${i === startIndex ? 'Now' : timeStr}</div>
       <div class="hourly-icon">${itemMeta.svg}</div>
       <div class="hourly-temp">${temp}°</div>
     `;
     
     els.hourlyForecast.appendChild(div);
  }
}
