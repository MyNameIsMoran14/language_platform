/*тест карточки*/ 
document.addEventListener("DOMContentLoaded", function () {
  const correctAnswer = "在";
  const cards = document.querySelectorAll(".card");
  const feedback = document.querySelector(".feedback");

  if (cards.length > 0 && feedback) {
    cards.forEach(card => {
      card.addEventListener("click", () => {
        if (card.textContent === correctAnswer) {
          feedback.textContent = "Верно!";
          feedback.style.color = "#00ff88";
        } else {
          feedback.textContent = "Неправильно. Попробуй ещё.";
          feedback.style.color = "#ff5050";
        }
      });
    });
  }
});



// let canvas = document.getElementById('draw-area');
// let ctx = canvas.getContext('2d');
// let drawing = false;

// canvas.addEventListener('mousedown', () => drawing = true);
// canvas.addEventListener('mouseup', () => drawing = false);
// canvas.addEventListener('mousemove', draw);

// function draw(e) {
//   if (!drawing) return;
//   ctx.fillStyle = "black";
//   ctx.beginPath();
//   ctx.arc(e.offsetX, e.offsetY, 4, 0, 2 * Math.PI);
//   ctx.fill();
// }

// function submitDrawing() {
//   let imgData = canvas.toDataURL('image/png');
//   fetch('/recognize', {
//     method: 'POST',
//     headers: {'Content-Type': 'application/json'},
//     body: JSON.stringify({ image: imgData })
//   })
//   .then(res => res.json())
//   .then(data => alert("Распознанный иероглиф: " + data.character));
// }


//db scan