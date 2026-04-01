const form = document.querySelector("form");
const seriesContainer = document.getElementById("series-container");
function searchShows(query) {
  const url = `/api/search?q=${encodeURIComponent(query)}`;
  fetch(url)
    .then((response) => response.json())
    .then((results) => {
      seriesContainer.innerHTML = "";
      results.forEach((show) => {
        const rating = show.rating ? show.rating : null;
        const genres = show.genres ? show.genres.join(", ") : "-";
        const image = show.image
          ? `<img src="${show.image}" width="300">`
          : `<div class="no-poster"></div>`;

        const showDiv = document.createElement("div");
        showDiv.classList.add("serie");

        showDiv.innerHTML = `
                    <a href="${show.url || "#"}" target="_blank">
                       ${image}
                    </a>
                    <h3>${show.name}</h3>
                    <p><strong>Langue:</strong> ${show.language || "-"}</p>
                    <p><strong>Genres:</strong> ${genres}</p>
                    <p><strong>Statut:</strong> ${show.status || "-"}</p>
                    <div class="rating-bar-container">
                    <div class="rating-bar" style="width: ${rating ? rating * 10 : 0}%"></div>
                    <span class="rating-label">${rating ? rating + " ★" : "Pas de note"}</span>
                    </div>
                `;
        showDiv.addEventListener("click", function () {
          window.location.href = `/detail?id=${show.id}`;
        });
        seriesContainer.appendChild(showDiv);
      });
    })
    .catch((error) => {
      console.log("Erreur :", error);
    });
}

document
  .getElementById("search-button")
  .addEventListener("click", function (event) {
    event.preventDefault();
    const query = document.getElementById("search-input").value.trim();
    if (!query) return;
    sessionStorage.setItem("histoire", query);
    searchShows(query);
  });

window.addEventListener("load", function () {
  const lastSearch = sessionStorage.getItem("histoire");
  if (!lastSearch) return;
  document.getElementById("search-input").value = lastSearch;
  searchShows(lastSearch);
});

document.getElementById("home-page").addEventListener("click", function () {
  window.location.href = "/home-test";
});
