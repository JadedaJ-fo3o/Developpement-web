document.addEventListener("DOMContentLoaded", loadWatchlist)

async function loadWatchlist() {
    const res = await fetch("/api/watchlist")
    const data = await res.json()

    renderRegardes(data.regardes)
    renderAvoirs(data.avoirs)
}

function renderRegardes(regardes) {
    const container = document.getElementById("regarde-container")
    container.innerHTML = ""

    regardes.forEach(show => {
        const image = show.image_url || ""
        const rating = Number(show.rating_value) || 0

        const div = document.createElement("div")
        div.classList.add("serie")

        div.innerHTML = `
            <img src="${image}" alt="${show.name_serie}">
            <h3>${show.name_serie}</h3>

            <div class="rating-bar-container">
                <div class="rating-bar" style="width: ${rating * 20}%"></div>
                <span class="rating-label">${rating}/5</span>
            </div>

            <div class="action-buttons">
                <button class="btn-modifier">Changer mon avis</button>
                <button class="btn-supprimer">Supprimer</button>
            </div>
        `

        const btnModifier = div.querySelector(".btn-modifier")
        const btnSupprimer = div.querySelector(".btn-supprimer")

        btnModifier.addEventListener("click", function () {
            goDetail(show.external_id)
        })

        btnSupprimer.addEventListener("click", async function () {
            await deleteRegarde(show.external_id)
        })

        container.appendChild(div)
    })
}

function renderAvoirs(avoirs) {
    const container = document.getElementById("avoir-container")
    container.innerHTML = ""

    avoirs.forEach(show => {
        const image = show.image_url || ""

        const div = document.createElement("div")
        div.classList.add("serie")

        div.innerHTML = `
            <img src="${image}" alt="${show.name_serie}">
            <h3>${show.name_serie}</h3>

            <div class="action-buttons">
                <button class="btn-ajouter-vu">Ajouter comme vu</button>
                <button class="btn-supprimer">Supprimer</button>
            </div>
        `

        const btnAjouterVu = div.querySelector(".btn-ajouter-vu")
        const btnSupprimer = div.querySelector(".btn-supprimer")

        btnAjouterVu.addEventListener("click", function () {
            goDetail(show.external_id)
        })

        btnSupprimer.addEventListener("click", async function () {
            await deleteAvoir(show.external_id)
        })

        container.appendChild(div)
    })
}

// 未来要改再说吧...
function goDetail(id) {
    window.location.href = "/detaille?id=" + id
}

async function deleteRegarde(id) {
    await fetch("/api/regarde/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            external_id: id
        })
    })

    loadWatchlist()
}

async function deleteAvoir(id) {
    await fetch("/api/avoir/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            external_id: id
        })
    })

    loadWatchlist()
}
