// modal.js

const loginModal = document.getElementById('loginModal');
const joinModal = document.getElementById('joinModal');

const closeLoginModal = document.getElementById('closeLoginModal');
const closeJoinModal = document.getElementById('closeJoinModal');
const openJoinModalFromLogin = document.getElementById('openJoinModalFromLogin');
const openLoginModalFromJoin = document.getElementById('openLoginModalFromJoin');

// Utility functions
export function openModal(modal) {
    if (!modal) return;
    modal.classList.remove('hidden');

    requestAnimationFrame(() => {
        modal.classList.remove('opacity-0');
        modal.querySelector('div').classList.replace('scale-90', 'scale-100');
    });
}

export function closeModal(modal) {
    if (!modal) return;
    modal.classList.add('opacity-0');
    modal.querySelector('div').classList.replace('scale-100', 'scale-90');

    setTimeout(() => modal.classList.add('hidden'), 300);
}

// Attach login buttons
['loginBtn', 'loginBtnMobile', 'loginBtnCTA'].forEach(id => {
    document.getElementById(id)?.addEventListener('click', () => openModal(loginModal));
});

// Attach join buttons
['joinBtn', 'joinBtnHero', 'joinBtnCTA'].forEach(id => {
    document.getElementById(id)?.addEventListener('click', () => openModal(joinModal));
});

// Close buttons
closeLoginModal?.addEventListener('click', () => closeModal(loginModal));
closeJoinModal?.addEventListener('click', () => closeModal(joinModal));

// Switch modals
openJoinModalFromLogin?.addEventListener('click', () => {
    closeModal(loginModal);
    setTimeout(() => openModal(joinModal), 300);
});

openLoginModalFromJoin?.addEventListener('click', () => {
    closeModal(joinModal);
    setTimeout(() => openModal(loginModal), 300);
});

// Click outside to close
window.addEventListener('click', (e) => {
    if (e.target === loginModal) closeModal(loginModal);
    if (e.target === joinModal) closeModal(joinModal);
});
