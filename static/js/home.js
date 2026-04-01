document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("home-search-form");
  const input = document.getElementById("search-input");

  if (!form || !input) {
    return;
  }

  loadTodaySchedule()

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const query = input.value.trim();
    if (!query) {
      return;
    }

    window.location.href = `/search?q=${encodeURIComponent(query)}`;
  });
});

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
      console.error("Erreur lors du chargement des programmes d'aujourd'hui:", err);
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
