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


            detailContainer.innerHTML = `
                <h1>${show.name}</h1>
                <div class="information-container">
                    <div class="poster-container">
                    <img src="${show.image}" width="300">
                    </div>

                    <div class="infos-series">
                    <p><strong>Réalisateur:</strong> ${show.directors.join(', ') || '————'}</p>
                    <p><strong>Scénaristes:</strong> ${show.writers.join(', ') || '————'} </p>
                    <p><strong>Date de sortie:</strong> ${show.premiered}</p>
                    <p><strong>Langue:</strong> ${show.language}</p>
                    <p><strong>Genres:</strong> ${show.genres.join(', ')}</p>
                    <p><strong>Statut:</strong> ${show.status}</p>
                    <p><strong>Langue:</strong> ${show.language}</p>
                    <p><strong>Pays:</strong> ${show.country || '-'}</p>
                    <p><strong>Rating par TVMaze:</strong> ${show.rating || 'Pas de note'}</p>
                    <p><strong>Surnoms:</strong> ${show.akas.join(', ')}</p>
                    <p><strong>Cast:</strong> ${show.cast.map(c => c.name).join(', ')}</p>
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

