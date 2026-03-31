function inscrire() {
    document.getElementById('form_connect').style.display = 'none';
    document.getElementById('form_inscrire').style.display = 'block';
}

function connect() {
    document.getElementById('form_connect').style.display = 'block';
    document.getElementById('form_inscrire').style.display = 'none';
}

document.addEventListener("DOMContentLoaded", () => {

    // LOGIN  提交监听
    document.getElementById('form_connect').querySelector('form')
        .addEventListener("submit", async (event) => {
            event.preventDefault();
            const data = Object.fromEntries(new FormData(event.target));

            const res = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                window.location.href = "/";
            } else {
                alert("Vos identifiants sont incorrects ou votre compte n'existe pas.");
            }
        });

    // REGISTER 监听
    document.getElementById('form_inscrire').querySelector('form')
        .addEventListener("submit", async (event) => {
            event.preventDefault();
            const data = Object.fromEntries(new FormData(event.target));

            const res = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                window.location.href = "/";
            } else {
                const json = await res.json();
                alert(json.error || "Vous avez déjà un compte avec ces identifiants.");
            }
        });
});