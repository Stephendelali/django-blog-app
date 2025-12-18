function showPremiumToast(message) {
  const toast = document.getElementById('premiumToast');
  const text = document.getElementById('premiumToastText');

  text.textContent = message;

  toast.classList.remove('opacity-0', 'translate-y-4');
  toast.classList.add('opacity-100', 'translate-y-0');

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-4');
    toast.classList.remove('opacity-100');
  }, 2000);
}
