document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("recommendation-form");
  const input = document.getElementById("recommendation-input");
  const resultContainer = document.getElementById(
    "recommendation-result-container",
  );
  const errorBox = document.getElementById("recommendation-error");
  // ===================================================
  // Gestionnaire d'événement du formulaire
  // ===================================================
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = input.value.trim();
    if (!question) return;

    errorBox.style.display = "none";
    resultContainer.innerHTML = "<p>Chargement...</p>";

    try {
      // Envoie la question au backend
      const response = await fetch("/api/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ question }), //->string
      });

      const contentType = response.headers.get("content-type") || ""; //pour les vides
      let data = {};

      if (contentType.includes("application/json")) {
        data = await response.json();
      } else {
        const text = await response.text();
        data = { error: text || "Réponse serveur invalide" };
      }

      // Gère les erreurs
      if (response.status === 401) {
        errorBox.textContent =
          "Session expirée. Reconnectez-vous puis réessayez.";
        errorBox.style.display = "block";
        resultContainer.innerHTML = "";
        return;
      }

      if (!response.ok) {
        errorBox.textContent = data.error || "Erreur serveur";
        errorBox.style.display = "block";
        resultContainer.innerHTML = "";
        return;
      }

      // Affiche les résultats
      resultContainer.innerHTML = "";
      renderRecommendationTable(data);
    } catch (error) {
      // Erreurs
      errorBox.textContent = "Erreur réseau. Veuillez réessayer.";
      errorBox.style.display = "block";
      resultContainer.innerHTML = "";
      console.error(
        "Erreur lors de la récupération des recommandations:",
        error,
      );
    }
  });
});

// ===================================================
// 左边图片 genre note titre | 右边理由
// Gauche : informations de la série (image, titre, genres, note)
// Droite : raison de la recommandation
// ===================================================
function renderRecommendationTable(data) {
  let items = [];
  if (Array.isArray(data.items)) {
    items = data.items;
  }
  const message = data.message || "";

  const resultContainer = document.getElementById(
    "recommendation-result-container",
  );

  // le cas sans résultats
  if (items.length === 0) {
    const displayMessage = message || "Aucune recommandation pour le moment.";
    const messageDiv = document.createElement("div");
    messageDiv.className = "recommendation-answer";
    messageDiv.textContent = displayMessage;
    resultContainer.appendChild(messageDiv);
    return;
  }

  if (message) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "recommendation-answer";
    messageDiv.textContent = message;
    resultContainer.appendChild(messageDiv);
  }

  //table
  const table = document.createElement("table");
  table.className = "recommendation-table";

  const thead = document.createElement("thead");
  const headRow = document.createElement("tr");

  const showHeader = document.createElement("th");
  showHeader.textContent = "Série (TVMaze)";
  const reasonHeader = document.createElement("th");
  reasonHeader.textContent = "Raison de recommandation";

  headRow.appendChild(showHeader);
  headRow.appendChild(reasonHeader);
  thead.appendChild(headRow);

  const tbody = document.createElement("tbody");
  items.forEach((item) => {
    tbody.appendChild(createRecommendationRow(item)); //->tr
  });

  table.appendChild(thead);
  table.appendChild(tbody);
  resultContainer.appendChild(table);
}

function createRecommendationRow(item) {
  //  items.append(
  //       {
  //           "name": show.get("name") or title,
  //           "image": show.get("image"),
  //           "rating": show.get("rating"),
  //           "url": show.get("url"),
  //           "genres": show.get("genres", []),
  //           "reason": reason,
  //       }
  const name = item.name || "-";
  const reason = item.reason || "-";
  const genres = formatGenres(item.genres);
  const ratingText = formatRating(item.rating);
  const image = item.image || "";
  const url = item.url || "#";

  const row = document.createElement("tr");
  const showCell = document.createElement("td");
  const reasonCell = document.createElement("td");

  const showWrapper = document.createElement("div");
  showWrapper.className = "recommendation-show-cell";

  //image peut être vide
  if (image) {
    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";

    const img = document.createElement("img");
    img.src = image;
    img.alt = name;
    img.className = "recommendation-show-image";

    link.appendChild(img);
    showWrapper.appendChild(link);
  }
  //informations
  const meta = document.createElement("div");
  meta.className = "recommendation-show-meta";

  const titleDiv = document.createElement("div");
  titleDiv.className = "recommendation-show-title";
  titleDiv.textContent = name;

  const genresDiv = document.createElement("div");
  genresDiv.className = "recommendation-show-sub";
  genresDiv.textContent = `Genres : ${genres}`;

  const ratingDiv = document.createElement("div");
  ratingDiv.className = "recommendation-show-sub";
  ratingDiv.textContent = `Note : ${ratingText}`;

  meta.appendChild(titleDiv);
  meta.appendChild(genresDiv);
  meta.appendChild(ratingDiv);

  showWrapper.appendChild(meta);
  showCell.appendChild(showWrapper);

  reasonCell.textContent = reason;

  row.appendChild(showCell);
  row.appendChild(reasonCell);

  return row;
}

// Formations
function formatGenres(genres) {
  if (!Array.isArray(genres) || genres.length === 0) {
    return "-";
  }
  return genres.join(", ");
}

function formatRating(rating) {
  if (rating === null || rating === undefined) {
    return "Pas de note";
  }
  return typeof rating === "number" ? `${rating} ★` : String(rating);
}
