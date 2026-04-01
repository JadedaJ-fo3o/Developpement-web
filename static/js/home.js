document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("home-search-form");
  const input = document.getElementById("search-input");
  const recommendationContainer = document.getElementById(
    "recommendation-content",
  );

  if (!form || !input) {
    return;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const query = input.value.trim();
    if (!query) {
      return;
    }

    window.location.href = `/search?q=${encodeURIComponent(query)}`;
  });

  if (recommendationContainer) {
    loadHomeRecommendations(recommendationContainer);
  }
});

// home page recommendation
function loadHomeRecommendations(container) {
  container.innerHTML = "<p>Chargement des recommandations...</p>";

  fetch("/api/home-recommendations", {
    method: "GET",
    credentials: "same-origin",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch home recommendations");
      }
      return response.json();
    })
    .then((data) => {
      const items = Array.isArray(data.items) ? data.items : [];
      const message = data.message || "";

      container.innerHTML = "";

      if (message) {
        const hint = document.createElement("p");
        hint.textContent = message;
        hint.style.opacity = "0.85";
        hint.style.marginBottom = "12px";
        container.appendChild(hint);
      }

      if (items.length === 0) {
        const empty = document.createElement("p");
        empty.textContent = "Aucune recommandation disponible.";
        container.appendChild(empty);
        return;
      }

      const grid = document.createElement("div");
      grid.style.display = "grid";
      grid.style.gridTemplateColumns = "repeat(auto-fit, minmax(170px, 1fr))";
      grid.style.gap = "12px";

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

  const title = document.createElement("h4");
  title.textContent = name;
  title.style.margin = "0 0 6px";
  title.style.fontSize = "14px";
  card.appendChild(title);

  const ratingContainer = document.createElement("div");
  ratingContainer.className = "rating-bar-container";

  const ratingBar = document.createElement("div");
  ratingBar.className = "rating-bar";
  ratingBar.style.width = `${ratingWidth}%`;

  const ratingLabel = document.createElement("span");
  ratingLabel.className = "rating-label";
  ratingLabel.textContent = ratingText;

  ratingContainer.appendChild(ratingBar);
  ratingContainer.appendChild(ratingLabel);
  card.appendChild(ratingContainer);

  if (reason) {
    const text = document.createElement("p");
    text.textContent = reason;
    text.style.margin = "0";
    text.style.fontSize = "12px";
    text.style.opacity = "0.85";
    card.appendChild(text);
  }

  return card;
}
