document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("home-search-form");
  const input = document.getElementById("search-input");
  const recommendationContainer = document.getElementById(
    "recommendation-content",
  );

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

  loadTodaySchedule()

  form.addEventListener("submit", function (event) {
    event.preventDefault();

      items.forEach((item) => {
        grid.appendChild(createHomeRecommendationCard(item));
      });

      container.appendChild(grid);
    })
    .catch(() => {
      container.innerHTML = "<p>Impossible de charger les recommandations.</p>";
    });
}

//créer une carte de recommandation pour home page
function createHomeRecommendationCard(item) {
  const card = document.createElement("div");
  card.style.background = "rgba(0, 0, 0, 0.35)";
  card.style.border = "1px solid rgba(255, 255, 255, 0.2)";
  card.style.borderRadius = "10px";
  card.style.padding = "10px";

  const name = item.name || "-";

  //   <div class="rating-bar-container">
  //     <div class="rating-bar" style="width: ${rating ? rating * 10 : 0}%"></div>
  //     <span class="rating-label">${rating ? rating + " ★" : "Pas de note"}</span>
  //   </div>;

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

let offset = 0;
const limit = 5;

const nextBtn = document.getElementById("today-next");
if (nextBtn) {
  nextBtn.addEventListener("click", async () => {
    try {
      offset += limit; // Increment offset for next batch
      const res = await fetch(`/api/today-schedule?offset=${offset}&limit=${limit}`);
      const data = await res.json();

      if (!data || data.length === 0) {
        nextBtn.disabled = true;
        nextBtn.innerText = "Pas plus de programmes disponibles";
        return;
      }

      appendTodaySchedule(data);
      offset += limit;
    } catch (err) {
      console.error(
        "Erreur lors du chargement des programmes d'aujourd'hui:",
        err,
      );
    }
  });
}

function loadTodaySchedule(offset = 0, limit = 5) {
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

    // const image = item.image || "/static/img/no-image.png";
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

// document.addEventListener("DOMContentLoaded", loadTodaySchedule);
