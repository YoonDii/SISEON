$(function() {

	// Menu Tabular
	var $menu_tabs = $('.menu__tabs li a'); 
	$menu_tabs.on('click', function(e) {
		e.preventDefault();
		$menu_tabs.removeClass('active');
		$(this).addClass('active');

		$('.menu__item').fadeOut(300);
		$(this.hash).delay(300).fadeIn();
	});
});

document.querySelector(".menu__tabs").addEventListener('click', function(e) {
	const a = document.querySelector(".active").id
	const b = document.querySelector(".card")
	const c = document.querySelector("#gathering")
	const d = document.querySelector("#study")
	if(a === "모임"){
		c.setAttribute('class', 'option-active')
		d.setAttribute('class', 'option-inactive')
	}
	else{
		c.setAttribute('class', 'option-inactive')
		d.setAttribute('class', 'option-active')
	}
})