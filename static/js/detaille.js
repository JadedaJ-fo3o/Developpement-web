const params = new URLSearchParams(window.location.search)
const showId = params.get('id')
const detailContainer = document.getElementById('detaille-film')

if (!showId) {
    detailContainer.innerHTML = '<p>ID manquant.</p>'
} else {
    fetch(`/api/detail/${showId}`)
        .then(r => r.json())
        .then(show => {
            const summary = show.summary
                ? show.summary.replace(/<[^>]+>/g, '')
                : 'Pas de description.'
            const image = show.image 
                ? `<img src="${show.image}" width="300">` 
                : `<div class="no-poster-detaille"></div>`

            detailContainer.innerHTML = `
                <h1>${show.name}</h1>
                <div class="information-container">
                    <div class="poster-container">
                    ${image}
                    </div>

                    <div class="infos-series">
                    <p><strong>Réalisateur:</strong> ${show.directors.join(', ') || 'Non enregistré'}</p>
                    <p><strong>Scénaristes:</strong> ${show.writers.join(', ') || 'Non enregistré'} </p>
                    <p><strong>Date de sortie:</strong> ${show.premiered || 'Non enregistré'}</p>
                    <p><strong>Langue:</strong> ${show.language || 'Non enregistré'}</p>
                    <p><strong>Genres:</strong> ${show.genres.join(', ') || 'Non enregistré'}</p>
                    <p><strong>Statut:</strong> ${show.status || 'Non enregistré'}</p>
                    <p><strong>Langue:</strong> ${show.language || 'Non enregistré'}</p>
                    <p><strong>Pays:</strong> ${show.country || 'Non enregistré'}</p>
                    <p><strong>Rating par TVMaze:</strong> ${show.rating || 'Pas de note'}</p>
                    <p><strong>Surnoms:</strong> ${show.akas.join(', ') || 'Non enregistré'}</p>
                    <p><strong>Cast:</strong> ${show.cast.map(c => c.name).join(', ') || 'Non enregistré'}</p>
                    </div>
                </div>

                <div class="summary-container">
                <h3>Description:</h3>
                <p>${summary}</p>
                </div>
            `
        })
        .catch(err => {
            detailContainer.innerHTML = '<p>Erreur lors du chargement.</p>'
            console.error(err)
        })
}

// Source: https://docs.pingcode.com/baike/2406307
document.getElementById('back-button').addEventListener('click', function() {
    window.history.back()
})

document.getElementById('home-page').addEventListener('click', function() {
    window.location.href = '/home-test'
})