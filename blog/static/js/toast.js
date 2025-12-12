// toast.js

export function showToast(message, type = "success") {
    const container = document.getElementById("toastContainer");
    const toast = document.createElement("div");

    const colors = {
        success: "bg-green-600",
        error: "bg-red-600"
    };

    toast.className = `${colors[type]} text-white px-4 py-3 rounded-lg shadow-lg animate-slide-in flex items-center gap-3`;
    toast.innerHTML = `<span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("opacity-0", "translate-x-10");
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
