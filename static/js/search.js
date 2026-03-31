const form = document.querySelector('form')
const seriesContainer = document.getElementById('series-container')

document.getElementById('search-button').addEventListener('click', function(event) {
    event.preventDefault()
    const query = document.getElementById('search-input').value.trim()
    if (!query) return

    const url = `/api/search?q=${encodeURIComponent(query)}`
    fetch(url)
        .then(response => response.json())
        .then(results => {
            seriesContainer.innerHTML = ''
            results.forEach(show => {
                const image = show.image ? show.image.medium : ''
                const rating = show.rating ? show.rating.average : null
                const genres = show.genres ? show.genres.join(', ') : '-'

                const showDiv = document.createElement('div')
                showDiv.classList.add('serie')

                showDiv.innerHTML = `
                    <a href="${show.url || '#'}" target="_blank">
                        <img src="${image}" alt="${show.name}">
                    </a>
                    <h3>${show.name}</h3>
                    <p><strong>Langue:</strong> ${show.language || '-'}</p>
                    <p><strong>Genres:</strong> ${genres}</p>
                    <p><strong>Statut:</strong> ${show.status || '-'}</p>
                    <div class="rating-bar-container">
                    <div class="rating-bar" style="width: ${rating ? rating * 10: 0}%"></div>
                    <span class="rating-label">${rating ? rating + ' ★' : 'Pas de note'}</span>
                    </div>
                    <div class="action-buttons">
                        <select id="sentiment-${show.id}">
                            <option value="aime">Aimé</option>
                            <option value="neutre">Neutre</option>
                            <option value="non-aime">N'aime pas</option>
                        </select>
                        <button onclick="regarde(${show.id}, '${show.name}', '${image}', ${rating})">
                            Regardé
                        </button>
                        <button onclick="aVoir(${show.id}, '${show.name}', '${image}')">
                            A voir
                        </button>
                    </div>
                `
                seriesContainer.appendChild(showDiv)
            })
        })
        .catch(error => {
            console.log("Erreur :", error)
        })
})

function regarde(showId, showName, showImage, showRating) {
    const sentiment = document.getElementById(`sentiment-${showId}`).value
    console.log('Regarde :', showId, showName, sentiment)
    // à implémenter : POST /add
}

function aVoir(showId, showName, showImage) {
    console.log('A voir :', showId, showName)
    // à implémenter : POST /a-voir/add
}