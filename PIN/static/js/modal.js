const modal = document.getElementById("login-modal");
const loginButton = document.querySelector(".cabinet");

loginButton.addEventListener("click",function(e){
    e.preventDefault();
    modal.style.display = "flex";
});

 function closeModal() {
    modal.style.display = "none";
  }

  window.addEventListener("click", function (e) {
    if (e.target === modal) {
      closeModal();
    }
  });

function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.toggle-password');
    const isHidden = passwordInput.type === 'password';

    passwordInput.type = isHidden ? 'text' : 'password';
    toggleIcon.textContent = isHidden ? '👁' : '👁';
}

function openModal() {
    const modal = document.getElementById("login-modal");
    modal.classList.remove("fade-out"); // если было закрытие до этого
    modal.style.display = "flex";
}

function closeModal() {
    const modal = document.getElementById("login-modal");
    const content = modal.querySelector(".modal-content");


    modal.classList.add("fade-out");
    content.classList.add("fade-out");


    setTimeout(() => {
        modal.style.display = "none";
        modal.classList.remove("fade-out");
        content.classList.remove("fade-out");
    }, 300);
}

function handleRegister() {
  alert("Переход на форму регистрации");

}