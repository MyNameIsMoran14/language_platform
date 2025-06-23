const swiperText = new Swiper('.swiper', {
	speed: 1600,
	mousewheel: {},
	pagination: {
		el: '.swiper-pagination',
		clickable: true
	},
	navigation: {
		prevEl: '.swiper-button-prev',
		nextEl: '.swiper-button-next'
	}
})

// Пути к видео для каждого слайда
const videoSources = [
	'/static/media/japan.mp4',
	'/static/media/china.mp4',
	'/static/media/korea.mp4',
	'/static/media/thailand.mp4'
]

const video = document.querySelector('.video-background')
let currentSlideIndex = 0

// Функция плавной смены видео
function switchVideoWithFade(newSrc) {
	// Добавляем класс затухания
	video.classList.add('fade-out')

	// Через 600 мс (длительность transition) меняем видео
	setTimeout(() => {
		video.pause()
		video.setAttribute('src', newSrc)
		video.load()

		// После загрузки — воспроизвести и проявить
		video.oncanplay = () => {
			video.play()
			video.classList.remove('fade-out')
			video.classList.add('fade-in')

			// Через небольшой интервал убираем fade-in
			setTimeout(() => {
				video.classList.remove('fade-in')
			}, 600)
		}
	}, 600)
}

// Обновляем видео при смене слайда
swiperText.on('slideChangeTransitionEnd', function () {
	const newIndex = this.realIndex
	currentSlideIndex = newIndex
	const newSrc = videoSources[newIndex]

	if (video.getAttribute('src') !== newSrc) {
		switchVideoWithFade(newSrc)
	}
})

// Повтор видео при окончании (если пользователь остался на этом слайде)
video.addEventListener('ended', () => {
	if (swiperText.realIndex === currentSlideIndex) {
		video.currentTime = 0
		video.play()
	}
})

/*переход на о нас*/
function scrollToAbout() {
    document.getElementById('about').scrollIntoView({
      behavior: 'smooth'
	});
}

/*знаешь что такое безумие? при каждом заходе на секцию - анимка снова (каюсь,вернула до одного воспроизведения)*/
const image = document.querySelector('.about-image img');
let animationPlayed = false;

const observer = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animationPlayed) {
        image.style.animation = 'fadeInImage 1.4s ease-out forwards';
        animationPlayed = true;
        observer.unobserve(image); // больше не наблюдаем, чтобы анимация не запускалась повторно
      }
    });
  },
  { threshold: 0.5 }
);

observer.observe(image);


/*тест карточки*/ 
document.addEventListener("DOMContentLoaded", function () {
	const correctAnswer = "在";
	const cards = document.querySelectorAll(".card");
	const feedback = document.querySelector(".feedback");

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
});