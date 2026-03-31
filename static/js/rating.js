// ===== 1. 获取 ID =====
const params = new URLSearchParams(window.location.search)
const id = params.get("id")

if (!id) {
    alert("ID manquant")
}


// ===== 2. 测试用：调用 TVMaze API =====
fetch(`https://api.tvmaze.com/shows/${id}`)
    .then(res => res.json())
    .then(show => {

        // 👉 显示节目数据（模拟你同学做的）
        document.getElementById("title").innerText = show.name

        const img = show.image ? show.image.medium : ""
        document.getElementById("poster").src = img

        document.getElementById("info").innerText =
            "Langue: " + (show.language || "-") +
            " | Genres: " + (show.genres ? show.genres.join(", ") : "-")

        // 👉 保存给后面用
        window.currentShow = show
    })


// ===== 3. 提交评分 =====

document.getElementById("submit").addEventListener("click", async function () {

    const rating = document.getElementById("rating").value
    const commentaire = document.getElementById("commentaire").value

    console.log("SENDING:", {
        external_id: id,
        rating_value: rating,
        commentaire: commentaire
    })

    const res = await fetch("/api/regarde/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            external_id: id,
            name_serie: "TEST",
            image_url: "",
            rating_value: rating,
            commentaire: commentaire
        })
    })

    const data = await res.json()
    console.log("RESPONSE:", data)

    // 👉 返回列表页
    window.location.href = "/"
})