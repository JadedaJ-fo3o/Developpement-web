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


// ===== 1. 取 id =====
let currentShow = null

// ===== 2. 加载数据 =====
fetch(`/api/detail/${showId}`)
    .then(r => r.json())
    .then(show => {
        currentShow = show
    })

// ===== 4. Regarde按钮 =====
document.getElementById("btn-evaluer")
    .addEventListener("click", function () {

    if (!currentShow) {
        alert("Chargement...")
        return
    }

    const input = document.querySelector('input[name="rating"]:checked')
    const rating = input ? input.value : null

    if (!rating) {
        alert("Choisissez une note")
        return
    }

    const commentaire = document.getElementById("commentaire").value

    fetch("/api/regarde/update", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            external_id: showId,
            name_serie: currentShow.name,
            image_url: currentShow.image?.medium || currentShow.image || "",
            rating_value: rating,
            commentaire: commentaire
        })
    })
    .then(() => fetch("/api/avoir/delete", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ external_id: showId })
    }))
    .then(() => location.reload())
})


// ===== 5. Avoir按钮 =====
document.getElementById("btn-avoir").onclick = function () {

    fetch("/api/avoir/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            external_id: showId,
            name_serie: currentShow.name,
            image_url: currentShow.image
        })
    })
    .then(() => location.reload())
}


// ===== 6. 按钮状态 =====
function initButtons() {

    fetch(`/api/regarde/get_one?external_id=${showId}`)
        .then(res => res.json())
        .then(data => {

            if (data && data.external_id) {

                document.getElementById("btn-avoir").disabled = true
                document.getElementById("btn-avoir").innerText = "Déja vu"
                document.getElementById("btn-evaluer").innerText = "Modifier"

            } else {

                fetch(`/api/avoir/get_one?external_id=${showId}`)
                    .then(res => res.json())
                    .then(data2 => {

                        if (data2 && data2.external_id) {
                            document.getElementById("btn-avoir").disabled = true
                            document.getElementById("btn-avoir").innerText = 'Dans "à voir" '
                        }
                    })
            }
        })
}


// ===== 7. 自动填充评分 =====
function loadExistingRating() {

    fetch(`/api/regarde/get_one?external_id=${showId}`)
        .then(res => res.json())
        .then(data => {

            if (data && data.rating_value) {

                const radio = document.querySelector(
                    `input[name="rating"][value="${data.rating_value}"]`
                )
                if (radio) radio.checked = true

                document.getElementById("commentaire").value =
                    data.commentaire || ""
            }
        })
}


// ===== 8. 启动 =====
initButtons()
loadExistingRating()