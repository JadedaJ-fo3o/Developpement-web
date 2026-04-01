document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("home-search-form");
  const input = document.getElementById("search-input");

  if (!form || !input) {
    return;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const query = input.value.trim();
    if (!query) {
      return;
    }

    sessionStorage.setItem("histoire", query);
    window.location.href = "/search";
  });
});


  let offset = 10;
const limit = 10;

const nextBtn = document.getElementById("today-next");

if (nextBtn) {
  nextBtn.addEventListener("click", async () => {
    try {
      const res = await fetch(`/today?offset=${offset}&limit=${limit}`);
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

function appendTodaySchedule(items) {
  const container = document.getElementById("today-schedule-content");
  if (!container) return;

  items.forEach(item => {
    const card = document.createElement("div");
    card.className = "today-card";

    const image = item.image || "/static/img/no-image.png";
    const episode = item.episode || "Épisode inconnu";
    const airtime = item.airtime ? `À ${item.airtime}` : "Heure inconnue";

    card.innerHTML = `
      <img src="${image}" class="today-img" />
      <div class="today-info">
        <p class="today-name">${item.name}</p>
        <p class="today-episode">${episode}</p>
        <p class="today-time">${airtime}</p>
      </div>
    `;

    container.appendChild(card);
  });
}
