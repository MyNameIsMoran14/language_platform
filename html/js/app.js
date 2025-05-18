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
	'media/japan.mp4',
	'media/china.mp4',
	'media/korea.mp4',
	'media/thailand.mp4'
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