window.addEventListener("pageshow", function () {
    loadWatchlist()
})

async function loadWatchlist() {
    const res = await fetch("/api/watchlist")
    const data = await res.json()

    renderRegardes(data.regardes)
    renderAvoirs(data.avoirs)
}

function renderRegardes(regardes) {
    const container = document.getElementById("regarde-container")
    container.innerHTML = ""

    regardes.slice().reverse().forEach(function(show) {

        const image = show.image_url || ""
        const rating = Number(show.rating_value) || 0

        const div = document.createElement("div")
        div.className = "serie"

        div.innerHTML = `
            <a href="/detaille?id=${show.external_id}">
                <img src="${image}" alt="${show.name_serie}">
            </a>

            <h3>${show.name_serie}</h3>

            <div class="rating-bar-container">
                <div class="rating-bar" style="width: ${rating * 20}%"></div>
                <span class="rating-label">${rating}/5</span>
            </div>

            <div class="btn-actions watchliste">
                <button id="btn-modifier-${show.external_id}" class="btn-action modifier">Changer mon avis</button>
                <button id="btn-supprimer-${show.external_id}" class="btn-action">Supprimer</button>
            </div>
        `

        container.appendChild(div)

        const btnModifier = div.querySelector("#btn-modifier-" + show.external_id)
        const btnSupprimer = div.querySelector("#btn-supprimer-" + show.external_id)

        btnModifier.addEventListener("click", function () {
            window.location.href = "/detail?id=" + show.external_id
        })

        btnSupprimer.addEventListener("click", async function () {
            await deleteRegarde(show.external_id)
        })

    })

    updateEmptyMessage("regarde-container", "regarde-empty")
}

function renderAvoirs(avoirs) {
    const container = document.getElementById("avoir-container")
    container.innerHTML = ""

    avoirs.slice().reverse().forEach(function(show) {

        const image = show.image_url || ""

        const div = document.createElement("div")
        div.className = "serie"

        div.innerHTML = `
            <a href="/detaille?id=${show.external_id}">
                <img src="${image}" alt="${show.name_serie}">
            </a>

            <h3>${show.name_serie}</h3>

            <div class="btn-actions avoir">
                <button id="btn-ajouter-vu-${show.external_id}" class="btn-action ajouter">Ajouter comme vu</button>
                <button id="btn-supprimer-${show.external_id}" class="btn-action">Supprimer</button>
            </div>
        `

        container.appendChild(div)

        const btnAjouterVu = div.querySelector("#btn-ajouter-vu-" + show.external_id)
        const btnSupprimer = div.querySelector("#btn-supprimer-" + show.external_id)

        btnAjouterVu.addEventListener("click", function () {
            window.location.href = "/detail?id=" + show.external_id
        })

        btnSupprimer.addEventListener("click", async function () {
            await deleteAvoir(show.external_id)
        })

    })

    updateEmptyMessage("avoir-container", "avoir-empty")
}

//空白消息
function updateEmptyMessage(containerId, messageId) {
    const container = document.getElementById(containerId)
    const message = document.getElementById(messageId)

    if (container.children.length === 0) {
        message.style.display = "null"
    } else {
        message.style.display = "none"
    }
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
