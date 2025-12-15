document.addEventListener('DOMContentLoaded', () => {
  // Open modals from buttons
  const openButtons = document.querySelectorAll('[data-open], #loginBtnMobile');
  
  openButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      let targetId = btn.dataset.open || 'loginModal'; // mobile login defaults to loginModal
      const modal = document.getElementById(targetId);
      modal.classList.remove('hidden', 'opacity-0', 'scale-95');
      setTimeout(() => modal.classList.add('opacity-100', 'scale-100'), 10);
    });
  });

  // Close modals
  document.querySelectorAll('#closeLoginModal, #closeJoinModal').forEach(btn => {
    btn.addEventListener('click', () => {
      const modal = btn.closest('[role="dialog"]');
      modal.classList.remove('opacity-100', 'scale-100');
      setTimeout(() => modal.classList.add('hidden', 'opacity-0', 'scale-95'), 300);
    });
  });

  // Switch modals
  const loginModal = document.getElementById('loginModal');
  const joinModal = document.getElementById('joinModal');

  document.getElementById('openJoinModalFromLogin')?.addEventListener('click', () => {
    loginModal.classList.remove('opacity-100', 'scale-100');
    setTimeout(() => {
      loginModal.classList.add('hidden', 'opacity-0', 'scale-95');
      joinModal.classList.remove('hidden', 'opacity-0', 'scale-95');
      setTimeout(() => joinModal.classList.add('opacity-100', 'scale-100'), 10);
    }, 300);
  });

  document.getElementById('openLoginModalFromJoin')?.addEventListener('click', () => {
    joinModal.classList.remove('opacity-100', 'scale-100');
    setTimeout(() => {
      joinModal.classList.add('hidden', 'opacity-0', 'scale-95');
      loginModal.classList.remove('hidden', 'opacity-0', 'scale-95');
      setTimeout(() => loginModal.classList.add('opacity-100', 'scale-100'), 10);
    }, 300);
  });

  // Prevent double submit
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;
    });
  });
});
