document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("login-modal");
  const loginButton = document.querySelector(".cabinet");
  const modalContent = modal.querySelector(".modal-content");


  loginButton?.addEventListener("click", function (e) {
    e.preventDefault();
    openModal();
  });


  window.addEventListener("click", function (e) {
    if (e.target === modal) {
      closeModal();
    }
  });


  window.togglePassword = function () {
    const passwordInput = document.getElementById("password");
    const toggleIcon = document.querySelector(".toggle-password");
    const isHidden = passwordInput.type === "password";

    passwordInput.type = isHidden ? "text" : "password";
    toggleIcon.textContent = isHidden ? "👁" : "👁";
  };

 
  window.openModal = function () {
    modal.classList.remove("fade-out");
    modal.style.display = "flex";
  };


  window.closeModal = function () {
    modal.classList.add("fade-out");
    modalContent.classList.add("fade-out");

    setTimeout(() => {
      modal.style.display = "none";
      modal.classList.remove("fade-out");
      modalContent.classList.remove("fade-out");
    }, 300);
  };


  window.handleRegister = function () {
    window.location.href = "/register"; 
  };
});

function openArticleModal() {
  document.getElementById('article-modal').style.display = 'flex';
}

function closeArticleModal() {
  document.getElementById('article-modal').style.display = 'none';
}

window.addEventListener('click', function (e) {
  const modal = document.getElementById('article-modal');
  if (e.target === modal) {
    closeArticleModal();
  }
});