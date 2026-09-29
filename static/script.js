/* ==========================================================================
   TRAFFIC JAM PREDICTION — INTERACTIVE SCRIPT (WARM LIGHT MODE)
   Tactile day pills, weather chips, friendly departure time formatting,
   animated Chart.js doughnut, and smart recommendations.
   ========================================================================== */

// ── Time of Day Helper ─────────────────────────────────────────
function formatHour(h) {
  const hourNum = parseInt(h);
  const period = hourNum >= 12 ? "PM" : "AM";
  const display12 = hourNum === 0 ? 12 : hourNum > 12 ? hourNum - 12 : hourNum;
  
  let label = "Midday Flow";
  if (hourNum >= 7 && hourNum <= 9) label = "Morning Peak Rush";
  else if (hourNum >= 16 && hourNum <= 18) label = "Evening Peak Rush";
  else if (hourNum >= 0 && hourNum <= 4) label = "Late Night / Empty";
  else if (hourNum >= 5 && hourNum <= 6) label = "Early Dawn";
  else if (hourNum >= 19 && hourNum <= 23) label = "Evening / Night";

  return `${display12}:00 ${period} (${label})`;
}

// ── Slider Display Sync ────────────────────────────────────────
const hourSlider = document.getElementById("hour");
const hourDisplay = document.getElementById("hour_display");
if (hourSlider && hourDisplay) {
  hourDisplay.textContent = formatHour(hourSlider.value);
  hourSlider.addEventListener("input", (e) => {
    hourDisplay.textContent = formatHour(e.target.value);
  });
}

const tempSlider = document.getElementById("temp_c");
const tempVal = document.getElementById("temp_c_val");
if (tempSlider && tempVal) {
  tempSlider.addEventListener("input", (e) => {
    const val = parseInt(e.target.value);
    tempVal.textContent = `${val > 0 ? "+" : ""}${val}°C`;
  });
}

const rainSlider = document.getElementById("rain_1h");
const rainVal = document.getElementById("rain_1h_val");
if (rainSlider && rainVal) {
  rainSlider.addEventListener("input", (e) => {
    const v = parseFloat(e.target.value);
    let desc = "Dry (0 mm)";
    if (v > 0 && v < 5) desc = `${v} mm (Light rain)`;
    else if (v >= 5 && v < 15) desc = `${v} mm (Moderate rain)`;
    else if (v >= 15) desc = `${v} mm (Heavy downpour)`;
    rainVal.textContent = desc;
  });
}

const cloudsSlider = document.getElementById("clouds_all");
const cloudsVal = document.getElementById("clouds_all_val");
if (cloudsSlider && cloudsVal) {
  cloudsSlider.addEventListener("input", (e) => {
    cloudsVal.textContent = `${e.target.value}%`;
  });
}

// ── Tactile Day-of-Week Pills ──────────────────────────────────
const dayPills = document.querySelectorAll(".day-pill");
const dayInput = document.getElementById("day_of_week");
const weekendInput = document.getElementById("is_weekend");
const weekendBadge = document.getElementById("weekend_badge");

dayPills.forEach(pill => {
  pill.addEventListener("click", () => {
    const day = parseInt(pill.getAttribute("data-day"));
    setDay(day);
  });
});

function setDay(day) {
  dayPills.forEach(p => {
    if (parseInt(p.getAttribute("data-day")) === day) {
      p.classList.add("active");
    } else {
      p.classList.remove("active");
    }
  });
  if (dayInput) dayInput.value = day;
  const isWknd = day >= 5 ? 1 : 0;
  if (weekendInput) weekendInput.value = isWknd;
  if (weekendBadge) {
    weekendBadge.textContent = isWknd ? "Weekend Schedule" : "Weekday Schedule";
    weekendBadge.style.color = isWknd ? "#B45309" : "#C85A17";
    weekendBadge.style.background = isWknd ? "#FFFBEB" : "#FDF3EB";
  }
}

// ── Tactile Weather Condition Chips ────────────────────────────
const weatherChips = document.querySelectorAll(".weather-chip");
const weatherInput = document.getElementById("weather_code");
const weatherLabel = document.getElementById("weather_label");

const weatherNames = {
  0: "Clear Sky",
  1: "Overcast / Cloudy",
  2: "Rainy / Stormy",
  3: "Snow / Freezing",
  4: "Mist / Fog / Reduced Visibility",
};

weatherChips.forEach(chip => {
  chip.addEventListener("click", () => {
    const code = parseInt(chip.getAttribute("data-weather"));
    setWeather(code);
  });
});

function setWeather(code) {
  weatherChips.forEach(c => {
    if (parseInt(c.getAttribute("data-weather")) === code) {
      c.classList.add("active");
    } else {
      c.classList.remove("active");
    }
  });
  if (weatherInput) weatherInput.value = code;
  if (weatherLabel) weatherLabel.textContent = weatherNames[code] || "Normal Weather";
}

// ── Holiday Switch ─────────────────────────────────────────────
function setHoliday(val) {
  const btnNo = document.getElementById("btn-holiday-no");
  const btnYes = document.getElementById("btn-holiday-yes");
  const holInput = document.getElementById("holiday_flag");
  const holHint = document.getElementById("holiday_hint");

  if (holInput) holInput.value = val;
  if (val === 1) {
    btnYes.classList.add("active");
    btnNo.classList.remove("active");
    if (holHint) holHint.textContent = "Holiday Transit Pattern";
  } else {
    btnNo.classList.add("active");
    btnYes.classList.remove("active");
    if (holHint) holHint.textContent = "Standard Schedule";
  }
}

// ── Quick-Try Presets ──────────────────────────────────────────
const presets = {
  rush: {
    hour: 8, day: 0, month: 9, weather: 0, temp: 18, rain: 0, clouds: 20, holiday: 0
  },
  rain: {
    hour: 17, day: 3, month: 10, weather: 2, temp: 12, rain: 12, clouds: 90, holiday: 0
  },
  night: {
    hour: 2, day: 5, month: 7, weather: 0, temp: 22, rain: 0, clouds: 10, holiday: 0
  },
  snow: {
    hour: 8, day: 1, month: 1, weather: 3, temp: -8, rain: 0, clouds: 95, holiday: 0
  },
};

function fillDemo(key) {
  const p = presets[key];
  if (!p) return;

  // Active preset chip highlight
  document.querySelectorAll(".preset-chip").forEach(btn => btn.classList.remove("active"));
  const activeBtn = document.getElementById("demo-" + key);
  if (activeBtn) activeBtn.classList.add("active");

  // Apply parameters
  if (hourSlider) {
    hourSlider.value = p.hour;
    if (hourDisplay) hourDisplay.textContent = formatHour(p.hour);
  }

  setDay(p.day);
  setWeather(p.weather);
  setHoliday(p.holiday);

  const monthSelect = document.getElementById("month");
  if (monthSelect) monthSelect.value = p.month;

  if (tempSlider) {
    tempSlider.value = p.temp;
    if (tempVal) tempVal.textContent = `${p.temp > 0 ? "+" : ""}${p.temp}°C`;
  }

  if (rainSlider) {
    rainSlider.value = p.rain;
    rainSlider.dispatchEvent(new Event("input"));
  }

  if (cloudsSlider) {
    cloudsSlider.value = p.clouds;
    if (cloudsVal) cloudsVal.textContent = `${p.clouds}%`;
  }
}

// ── Chart.js Doughnut Initialisation (Warm Light Mode) ─────────
const ctx = document.getElementById("probChart").getContext("2d");
const chart = new Chart(ctx, {
  type: "doughnut",
  data: {
    labels: ["Low Traffic", "Medium Traffic", "High Traffic"],
    datasets: [{
      data: [70, 25, 5],
      backgroundColor: ["#10B981", "#F59E0B", "#EF4444"],
      hoverBackgroundColor: ["#059669", "#D97706", "#DC2626"],
      borderColor: ["#FFFFFF", "#FFFFFF", "#FFFFFF"],
      borderWidth: 4,
      hoverOffset: 6,
    }],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          color: "#444950",
          padding: 16,
          font: { family: "'Plus Jakarta Sans', sans-serif", size: 12, weight: 600 },
          usePointStyle: true,
          pointStyle: "circle",
        },
      },
      tooltip: {
        backgroundColor: "#1C2024",
        titleFont: { family: "'Plus Jakarta Sans', sans-serif", size: 13, weight: 700 },
        bodyFont: { family: "'Plus Jakarta Sans', sans-serif", size: 12 },
        padding: 10,
        cornerRadius: 8,
        callbacks: {
          label: ctx => ` ${ctx.label}: ${ctx.parsed.toFixed(1)}%`,
        },
      },
    },
    cutout: "70%",
    animation: { animateRotate: true, duration: 800 },
  },
});

function updateChart(low, medium, high) {
  chart.data.datasets[0].data = [low, medium, high];
  chart.update("active");
}

// ── Prediction Pipeline ────────────────────────────────────────
document.getElementById("predict-btn").addEventListener("click", predict);

async function predict() {
  const payload = {
    hour:         parseInt(document.getElementById("hour").value),
    day_of_week:  parseInt(document.getElementById("day_of_week").value),
    month:        parseInt(document.getElementById("month").value),
    is_weekend:   parseInt(document.getElementById("is_weekend").value),
    holiday_flag: parseInt(document.getElementById("holiday_flag").value),
    weather_code: parseInt(document.getElementById("weather_code").value),
    temp_c:       parseFloat(document.getElementById("temp_c").value),
    rain_1h:      parseFloat(document.getElementById("rain_1h").value),
    clouds_all:   parseFloat(document.getElementById("clouds_all").value),
  };

  const spinner     = document.getElementById("spinner");
  const resultCard  = document.getElementById("result-card");
  const placeholder = document.getElementById("result-placeholder");
  const btn         = document.getElementById("predict-btn");

  spinner.style.display = "flex";
  btn.disabled = true;

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!data.success) throw new Error(data.error || "Inference server error");

    const p = data.result;
    displayResult(p);
    updateChart(p.probabilities.Low, p.probabilities.Medium, p.probabilities.High);

    if (placeholder) placeholder.style.display = "none";
    if (resultCard) {
      resultCard.classList.add("visible");
      resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

  } catch (err) {
    alert("Prediction Error: " + err.message);
  } finally {
    spinner.style.display = "none";
    btn.disabled = false;
  }
}

// ── Class Presentation & Smart Travel Advice ───────────────────
const classConfig = {
  Low: {
    bannerClass: "low",
    badge: "🟢 Low Congestion",
    headline: "Highway Flowing Freely",
    description: "Optimal travel conditions with minimal delays. Vehicles moving at normal corridor speeds (> 55 mph).",
    advice: "Great time to hit the road! Freeway traffic is free-flowing with minimal to no delays along the I-94 corridor.",
    color: "#15803D",
  },
  Medium: {
    bannerClass: "medium",
    badge: "🟡 Moderate Traffic",
    headline: "Steady Traffic Flow",
    description: "Moderate volume with periodic tap-braking near key merges and urban interchanges.",
    advice: "Moderate traffic volume. Speeds are steady, but consider adding 5–10 minutes buffer time for potential slowdowns near central interchanges.",
    color: "#B45309",
  },
  High: {
    bannerClass: "high",
    badge: "🔴 Heavy Traffic Alert",
    headline: "Severe Congestion Expected",
    description: "Dense rush-hour congestion with stop-and-go delays. Speeds significantly below posted speed limits.",
    advice: "Heavy rush hour congestion detected! Expect significant stop-and-go delays. Consider delaying departure or choosing alternate arterial routes.",
    color: "#B91C1C",
  },
};

function displayResult(p) {
  const cfg = classConfig[p.label] || classConfig["Low"];

  // Banner
  const banner = document.getElementById("status-banner");
  banner.className = `traffic-status-banner ${cfg.bannerClass}`;

  document.getElementById("result-badge").textContent = cfg.badge;
  document.getElementById("result-headline").textContent = cfg.headline;
  document.getElementById("result-description").textContent = cfg.description;

  // Confidence
  document.getElementById("conf-pct").textContent = p.confidence.toFixed(1) + "%";
  const confFill = document.getElementById("confidence-fill");
  confFill.style.width = p.confidence + "%";
  confFill.style.backgroundColor = cfg.color;

  // Probabilities
  document.getElementById("prob-low").textContent    = p.probabilities.Low.toFixed(1) + "%";
  document.getElementById("prob-medium").textContent = p.probabilities.Medium.toFixed(1) + "%";
  document.getElementById("prob-high").textContent   = p.probabilities.High.toFixed(1) + "%";

  // Advice
  document.getElementById("advice-text").textContent = cfg.advice;
}

// ── Status & Graphs Setup ──────────────────────────────────────
async function initPage() {
  try {
    const r = await fetch("/api/status");
    const d = await r.json();
    const banner = document.getElementById("model-banner");
    if (d.model_ready && banner) banner.style.display = "none";

    if (d.graphs) {
      const ts = "?t=" + Date.now();
      const setGraph = (id, src) => {
        const el = document.getElementById("graph-" + id);
        if (el) el.src = src;
      };
      setGraph("accuracy",  "/static/graphs/accuracy.png" + ts);
      setGraph("loss",      "/static/graphs/loss.png" + ts);
      setGraph("confusion", "/static/graphs/confusion_matrix.png" + ts);
    }
  } catch (_) {}
}

window.addEventListener("DOMContentLoaded", initPage);
