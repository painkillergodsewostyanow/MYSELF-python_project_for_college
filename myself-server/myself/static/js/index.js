new Swiper('.image-slider1', {

	initialSlide: 2,

	loop: true,

	navigation: {

      prevEl: '.swiper-prev1'

    },

	autoplay: {

		delay: 3000,
		disableOnIteraction: false,
		reverseDirection: true,

	},
});

new Swiper('.image-slider2', {

	initialSlide: 2,

	loop: true,
	navigation: {

      prevEl: '.swiper-prev2'

    },
	autoplay: {

		delay: 3000,
		disableOnIteraction: false,
		reverseDirection: true,

	},
});