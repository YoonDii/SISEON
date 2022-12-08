//좋아요
const likeBtn = document.querySelector('#like-btn')
likeBtn.addEventListener('click', function (event) {
  axios({
    method: 'get',
    url: `/gathering/${event.target.dataset.likeId}/like/`
  })
    .then(response => {
      console.log(response.data)
      if (response.data.isLike === true) {
        event.target.classList.add('bi-heart-fill')
        event.target.classList.add('articles-heart-fill')
        event.target.classList.remove('bi-heart')
        event.target.classList.remove('articles-heart')
        // console.log('좋아요')
      } else {
        event.target.classList.add('bi-heart')
        event.target.classList.add('articles-heart')
        event.target.classList.remove('bi-heart-fill')
        event.target.classList.remove('articles-heart-fill')
        // console.log('좋아요아님')
      }
      const likeCount = document.querySelector('#likes')
      likeCount.innerHTML = `<p>${response.data.like_cnt}</p>`
    })
})
