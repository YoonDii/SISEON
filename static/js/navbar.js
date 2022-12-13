const ham = document.querySelector('.ham');
const a_cate = document.querySelector('.a-cate');
const cate = document.querySelector('.cate');
const cate2 = document.querySelector('.cate2');
const nsearchBox = document.querySelector('.nsearch-box');

ham.addEventListener('click',() => {
  a_cate.classList.toggle('active');
  cate.classList.toggle('active');
  cate2.classList.toggle('active');
  nsearchBox.classList.toggle('active');
});

