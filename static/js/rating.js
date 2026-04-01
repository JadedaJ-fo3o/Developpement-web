// ===== 1. 取 id =====
const params = new URLSearchParams(window.location.search)
const id = params.get("id")

let currentShow = null



// ===== 2. 加载节目 =====
function loadShow() {
    fetch(`https://api.tvmaze.com/shows/${id}`)
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
            external_id: id,
            name_serie: currentShow.name,
            image_url: currentShow.image ? currentShow.image.medium : "",
            rating_value: rating,
            commentaire: commentaire
        })
    })
    .then(() => removeFromAvoir())
    .then(() => {
        alert("OK")
        window.location.href = "/"
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
            external_id: id,
            name_serie: currentShow.name,
            image_url: currentShow.image ? currentShow.image.medium : ""
        })
    })
    .then(() => {
        alert("Ajouté")
        window.location.href = "/"
    })
}


// ===== 7. 删除 avoir =====
function removeFromAvoir() {
    return fetch("/api/avoir/delete", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            external_id: id
        })
    })
}


// ===== 8. 初始化按钮状态 =====
function initAvoirButton() {

    const btn = document.getElementById("btn-avoir")

    // 👉 先查 REGARDE
    fetch(`/api/regarde/get_one?external_id=${id}`)
        .then(res => res.json())
        .then(data => {

            // ===== 已看过 =====
            if (data && data.external_id) {

                btn.innerText = "Supprimer"
                btn.onclick = function () {
                    removeFromAvoir().then(() => location.reload())
                }

            } else {

                // ===== 没看过 → 查 AVOIR =====
                fetch(`/api/avoir/get_one?external_id=${id}`)
                    .then(res => res.json())
                    .then(data2 => {

                        if (data2 && data2.external_id) {

                            btn.innerText = "Supprimer"
                            btn.onclick = function () {
                                removeFromAvoir().then(() => location.reload())
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

    fetch(`/api/regarde/get_one?external_id=${id}`)
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