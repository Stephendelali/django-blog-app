// login.js

import { closeModal } from "./modal.js";

const loginForm = document.getElementById('loginForm');

loginForm?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const csrfToken = this.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(this.action, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrfToken
            },
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            closeModal(document.getElementById("loginModal"));

            const redirect = sessionStorage.getItem("redirectAfterLogin") || window.location.href;
            sessionStorage.removeItem("redirectAfterLogin");
            window.location.href = redirect;
        } else {
            alert(result.error || "Invalid username or password.");
        }
    } catch (error) {
        alert("Login failed. Try again.");
    }
});
