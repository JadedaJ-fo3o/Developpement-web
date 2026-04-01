document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("home-search-form");
  const input = document.getElementById("search-input");

  if (!form || !input) {
    return;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const query = input.value.trim();
    if (!query) {
      return;
    }

    sessionStorage.setItem("histoire", query);
    window.location.href = "/search";
  });
});
