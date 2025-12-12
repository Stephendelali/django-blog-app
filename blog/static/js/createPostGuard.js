// createPostGuard.js

document.getElementById("openCreatePost")?.addEventListener("click", function (event) {
    event.preventDefault();
    const url = this.href;

    fetch(url).then(response => {
        if (response.status === 401) {
            sessionStorage.setItem("redirectAfterLogin", url);
            openModal(document.getElementById("loginModal"));
        } else {
            window.location.href = url;
        }
    });
});
