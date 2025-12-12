// googleAuth.js

function initGoogle() {
    google.accounts.id.initialize({
        client_id: "YOUR_GOOGLE_CLIENT_ID",
        ux_mode: "redirect",
        login_uri: "/accounts/google/login/",
    });

    google.accounts.id.renderButton(
        document.getElementById("googleSignInBtn"),
        {
            theme: "outline",
            size: "large",
            width: 300,
            text: "signin_with",
            shape: "rectangular"
        }
    );
}

window.addEventListener("load", () => setTimeout(initGoogle, 300));
