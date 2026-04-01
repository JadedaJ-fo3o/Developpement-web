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
                const image = show.image ? show.image : ''
                const rating = show.rating ? show.rating : null
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
                `
                showDiv.addEventListener('click', function() {
                    window.location.href = `/detail?id=${show.id}`
                })
                seriesContainer.appendChild(showDiv)
            })
        })
        .catch(error => {
            console.log("Erreur :", error)
        })
})



