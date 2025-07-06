/*тест карточки*/ 
let correct_answer=''
let correctCount = 0;
document.addEventListener("DOMContentLoaded", async function () {
  const sentenceEl = document.querySelector(".sentence");
  const cardsContainer = document.querySelector(".cards");
  const feedback = document.querySelector(".feedback");
  const loadingEl = document.querySelector(".loading-spinner");

  let exercises = [];
  let currentIndex = 0;

  try {
    const response = await fetch("/api/generate-quest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({})
    });

    if (!response.ok) throw new Error("Сервер вернул ошибку");

    const data = await response.json();
    exercises = data.exercises;
    correct_answer=data.exercises.correct_answer
    loadingEl.style.display = "none";
    showExercise();

  } catch (error) {
    console.error("Ошибка при получении задания:", error);
    feedback.textContent = "Ошибка загрузки задания.";
    feedback.style.color = "#ff5050";
  }

  function showExercise() {
    if (currentIndex >= exercises.length) {
      sentenceEl.textContent = "Все задания выполнены!";
      cardsContainer.innerHTML = "";
      feedback.textContent = "";
      return;
    }

    const exercise = exercises[currentIndex];

    sentenceEl.textContent = decodeUnicode(exercise.sentence);
    cardsContainer.innerHTML = "";
    feedback.textContent = "";

    exercise.options.forEach(option => {
      const button = document.createElement("button");
      button.className = "card";
      button.textContent = decodeUnicode(option);

      button.addEventListener("click", () => {
        if (button.textContent === decodeUnicode(exercise.correct_answer)) {
          feedback.textContent = "Верно!";
          feedback.style.color = "#00ff88";

          correctCount++;
          updateScore();

          setTimeout(() => {
            currentIndex++;
            showExercise();
          }, 1500); 
        } else {
          feedback.textContent = "Неправильно. Попробуй ещё.";
          feedback.style.color = "#ff5050";
        }
      });

      cardsContainer.appendChild(button);
    });
  }

  function decodeUnicode(str) {
    return str.replace(/\\u[\dA-F]{4}/gi, match =>
      String.fromCharCode(parseInt(match.replace(/\\u/g, ""), 16))
    );
  }
});


let correctAnswer = correct_answer; // ← сюда будет подставляться правильный ответ из API или массива

function updateScore() {
	const counter = document.getElementById('score-counter');

	counter.textContent = `Правильных ответов: ${correctCount}`;
}

function setupCardHandlers() {
	document.querySelectorAll('.card').forEach(card => {
		card.addEventListener('click', () => {
			const selected = card.textContent.trim();

			if (selected === correctAnswer) {
				correctCount++;
				updateScore();
				document.querySelector(".feedback").textContent = "✅ Верно!";
			} else {
				document.querySelector(".feedback").textContent = "❌ Неверно";
			}

			// Здесь можешь загрузить следующее задание
		});
	});
}

// Пример: при загрузке вопроса
function loadQuestion(data) {
	document.querySelector('.sentence').textContent = data.sentence;
	const cards = document.querySelectorAll('.card');

	data.options.forEach((option, i) => {
		cards[i].textContent = option;
	});

	correctAnswer = data.correct_answer;
}


/*уроки*/

document.addEventListener("DOMContentLoaded", function () {
	// Загрузка уроков при открытии страницы
	fetch('/get_chinese_lessons')
		.then(response => response.json())
		.then(data => {
			renderLessons(data);
		});

	// Отправка формы
	document.getElementById("article-form").addEventListener("submit", function (e) {
		e.preventDefault();

		const header = this.querySelector('input[name="header"]').value;
		const description = this.querySelector('textarea[name="description"]').value;

		fetch('/chinese_course_lessons', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ header, description })
		})
		.then(res => res.json())
		.then(data => {
			renderLessons(data); // Обновить список
			this.reset(); // Очистить форму
			closeArticleModal();
		});
	});
});

function renderLessons(lessons) {
	const container = document.getElementById("lessons-container");
	container.innerHTML = '';

	lessons.forEach(lesson => {
		const card = document.createElement("div");
		card.classList.add("article-card");
		
		card.innerHTML = `
			
			<h3>${lesson.title}</h3>
			<p>${lesson.description}</p>
		`;

		container.appendChild(card);
	});
}



document.addEventListener("DOMContentLoaded", () => {
	// Скрываем кнопку по умолчанию
	const addBtn = document.getElementById("add-lesson-btn");
	if (addBtn) addBtn.style.display = "none";

	// Проверка роли пользователя
	fetch('/get_user_role')
		.then(res => res.json())
		.then(data => {
			const role = data?.role;
			if (role === "teacher" || role === "admin") {
				if (addBtn) addBtn.style.display = "inline-block";
			}
		})
		.catch(err => {
			console.warn("Не удалось получить роль пользователя", err);
		});
});

fetch('/chinese_course_lessons', {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json'
	},
	body: JSON.stringify({ header, description })
})
.then(res => {
	if (!res.ok) {
		throw new Error("Сервер вернул ошибку");
	}
	return res.json();
})
.then(data => {
	renderLessons(data);
	document.getElementById("article-form").reset();
	closeArticleModal();
})
.catch(error => {
	console.error("Ошибка при добавлении урока:", error);
	alert("Ошибка: урок не добавлен");
});


/*НЕ НУЖНО*/

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