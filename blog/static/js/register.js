// register.js

import { closeModal } from "./modal.js";
import { showToast } from "./toast.js";

const joinForm = document.querySelector('#joinModal form');

joinForm?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const csrfToken = this.querySelector("[name=csrfmiddlewaretoken]").value;
    const submitBtn = joinForm.querySelector("button[type=submit]");

    submitBtn.disabled = true;
    submitBtn.textContent = "Creating...";

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
            showToast("Account created successfully!");
            closeModal(document.getElementById("joinModal"));

            setTimeout(() => window.location.reload(), 1000);
        } else {
            alert(result.error || "Registration failed.");
        }
    } catch (error) {
        alert("Network error.");
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Join";
    }
});
