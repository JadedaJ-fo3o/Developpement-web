document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("home-search-form");
  const input = document.getElementById("search-input");
  const recommendationContainer = document.getElementById(
    "recommendation-content",
  );

  loadTodaySchedule(0, 5);

  if (form && input) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();

      const query = input.value.trim();
      if (!query) {
        return;
      }

      window.location.href = `/search?q=${encodeURIComponent(query)}`;
    });
  }

  if (recommendationContainer) {
    loadHomeRecommendations(recommendationContainer);
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
      items.forEach((item) => {
        grid.appendChild(createHomeRecommendationCard(item));
      });

      container.appendChild(grid);
    })
    .catch(() => {
      container.innerHTML = "<p>Impossible de charger les recommandations.</p>";});

});

let offset = 5;
const limit = 5;

document.getElementById("today-next").addEventListener("click", async function () {
  try {
    const res = await fetch(`/api/today-schedule?offset=${offset}&limit=${limit}`);
    const data = await res.json();

    if (!data || data.length === 0) {
      this.disabled = true;
      this.innerText = "Pas plus de programmes disponibles";
      return;
    }

    appendTodaySchedule(data);
    offset += limit;
  } catch (err) {
    console.error("Erreur:", err);
  }
});


// Aujourd'hui à l'affiche
function loadTodaySchedule(offset, limit) {
  fetch(`/api/today-schedule?offset=${offset}&limit=${limit}`)
    .then(res => res.json())
    .then(data => appendTodaySchedule(data))
    .catch(err => console.error("Erreur chargement today-schedule:", err));
}
function appendTodaySchedule(items) {
  const container = document.getElementById("today-schedule-content");
  if (!container) return;
  
  items.forEach(item => {
    const card = document.createElement("div");
    card.className = "today-card";

    const imageHTML = item.image
      ? `<img src="${item.image}" class="today-img" id="poster-${item.show_id}"/>`
      : `<div class="no-poster" id="poster-${item.show_id}"></div>`
    const episode = item.episode || "Épisode inconnu";
    const airtime = item.airtime ? `À ${item.airtime}` : "Heure inconnue";

    card.innerHTML = `
      ${imageHTML}
      <div class="today-info">
        <h3 class="today-name">${item.name}</h3>
        <p class="today-episode"><strong>${episode}</strong></p>
        <p class="today-time">Horaire: ${airtime}</p>
      </div>
    `;

    container.appendChild(card);

    card.style.cursor = "pointer";
    card.addEventListener("click", function () {
      window.location.href = "/detail?id=" + item.show_id;
    });
  });
}

document.querySelectorAll(".ranking-item").forEach(function(card) {
  // card.style.cursor = "pointer";
  card.addEventListener("click", function() {
    const id = this.dataset.id;
    window.location.href = "/detail?id=" + id;
  });
});

document.querySelectorAll(".ranking-item-week").forEach(function(card) {
  card.style.cursor = "pointer";
  card.addEventListener("click", function() {
    const id = this.dataset.id;
    window.location.href = "/detail?id=" + id;
  });
});

// Recommandations pour vous
//créer une carte de recommandation
function createHomeRecommendationCard(item) {
  const card = document.createElement("div");
  card.style.background = "rgba(0, 0, 0, 0.35)";
  card.style.border = "1px solid rgba(255, 255, 255, 0.2)";
  card.style.borderRadius = "10px";
  card.style.padding = "10px";

  const name = item.name || "-";
  const ratingNumber = Number(item.rating);
  const hasRating =
    !isNaN(ratingNumber) && ratingNumber >= 0 && ratingNumber <= 10;
  const ratingText = hasRating ? `${ratingNumber} ★` : "Pas de note";
  const ratingWidth = hasRating
    ? Math.max(0, Math.min(100, ratingNumber * 10))
    : 0;

  const ratingContainer = document.createElement("div");
  ratingContainer.className = "rating-bar-container";

  const ratingBar = document.createElement("div");
  ratingBar.className = "rating-bar";
  ratingBar.style.width = `${ratingWidth}%`;

  const ratingLabel = document.createElement("span");
  ratingLabel.className = "rating-label";
  ratingLabel.textContent = ratingText;

  const reason = item.reason || "";
  const showId = item.id;

  if (item.image) {
    const link = document.createElement("a");
    if (showId !== null && showId !== undefined && showId !== "") {
      link.href = `/detail?id=${encodeURIComponent(String(showId))}`;
    } else {
      link.href = item.url || "#";
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }

    const img = document.createElement("img");
    img.src = item.image;
    img.alt = name;
    img.style.width = "100%";
    img.style.display = "block";
    img.style.borderRadius = "8px";
    img.style.marginBottom = "8px";

    link.appendChild(img);
    card.appendChild(link);
  }
}