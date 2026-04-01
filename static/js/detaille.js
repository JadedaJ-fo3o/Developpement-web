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

const homeLink = document.getElementById('home-logo-link')
if (homeLink) {
    homeLink.addEventListener('click', function() {
        window.location.href = '/home-test'
    })
}


// ===== 1. 取 id =====
let currentShow = null



// ===== 2. 加载节目 =====
function loadShow() {
    fetch(`https://api.tvmaze.com/shows/${showId}`)
        .then(res => res.json())
        .then(show => {
            currentShow = show

            document.getElementById("title").innerText = show.name

            const img = show.image ? show.image.medium : ""
            document.getElementById("poster").src = img
        })
}


// ===== 3. 获取评分 =====
function getRating() {
    const input = document.querySelector('input[name="rating"]:checked')
    if (!input) return null
    return input.value
}


// ===== 4. 获取评论 =====
function getComment() {
    return document.getElementById("commentaire").value
}


// ===== 5. 提交评分（Regarde）=====
function submitRegarde() {

    if (!currentShow) {
        alert("Chargement...")
        return
    }

    const rating = getRating()
    if (!rating) {
        alert("Choisissez une note")
        return
    }

    const commentaire = getComment()

    fetch("/api/regarde/update", {   // ✅ 已改
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            external_id: showId,
            name_serie: currentShow.name,
            image_url: currentShow.image ? currentShow.image.medium : "",
            rating_value: rating,
            commentaire: commentaire
        })
    })
    .then(() => removeFromAvoir())
    .then(() => {
        // alert("OK")
        location.reload()
    })
}


// ===== 6. 加入 avoir =====
function addAvoir() {

    if (!currentShow) {
        alert("Chargement...")
        return
    }

    fetch("/api/avoir/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            external_id: showId,
            name_serie: currentShow.name,
            image_url: currentShow.image ? currentShow.image.medium : ""
        })
    })
    .then(() => {
        // alert("Ajouté")
        location.reload()
        window.history.back()
    })
}


// ===== 7. 删除 avoir =====
function removeFromAvoir() {
    return fetch("/api/avoir/delete", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            external_id: showId
        })
    })
    .then(() => {
    // alert("Ajouté")
    window.history.back()
    })
}


// ===== 8. 初始化按钮状态 =====
function initAvoirButton() {

    const btn = document.getElementById("btn-avoir")

    // 👉 先查 REGARDE
    fetch(`/api/regarde/get_one?external_id=${showId}`)
        .then(res => res.json())
        .then(data => {

            // ===== 已看过 =====
            if (data && data.external_id) {

                btn.innerText = 'Supprimer de "vu"'

                btn.onclick = function () {
                    fetch("/api/regarde/delete", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            external_id: showId
                        })
                    })//.then(() => location.reload())
                    .then(() => {
                    // alert("Ajouté")
                    window.history.back()
                    })
                }

            } else {

                // ===== 查 AVOIR =====
                fetch(`/api/avoir/get_one?external_id=${showId}`)
                    .then(res => res.json())
                    .then(data2 => {

                        if (data2 && data2.external_id) {

                            btn.innerText = 'Supprimer de "à voir"'

                            btn.onclick = function () {
                                removeFromAvoir()//.then(() => location.reload())
                                .then(() => {
                                // alert("Ajouté")
                                window.history.back()
                                })
                            }

                        } else {

                            btn.innerText = "Ajouter à voir"
                            btn.onclick = addAvoir
                        }
                    })
            }
        })
}


// ===== 9. 自动填充评分 =====
function loadExistingRating() {

    fetch(`/api/regarde/get_one?external_id=${showId}`)
        .then(res => res.json())
        .then(data => {

            if (data && data.rating_value) {

                const radio = document.querySelector(
                    `input[name="rating"][value="${data.rating_value}"]`
                )
                if (radio) radio.checked = true

                document.getElementById("commentaire").value = data.commentaire || ""
            }
        })
        
}


// ===== 10. 绑定按钮 =====
function bindEvents() {
    document.getElementById("btn-evaluer").onclick = submitRegarde   // ✅ 修复
}


// ===== 11. 启动 =====
loadShow()
loadExistingRating()
initAvoirButton()
bindEvents()