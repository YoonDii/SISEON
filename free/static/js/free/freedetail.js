// 좋아요 비동기 구현
const likeFormTag = document.querySelector('.like-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


likeFormTag.addEventListener('submit', function (event) {
  event.preventDefault()
  axios({
    method: 'post',
    url: `/free/${likeFormTag.dataset.freePk}/like/`,
    headers: { 'X-CSRFToken': csrftoken },
  }).then((response) => {
    // 좋아요 아이콘 토글
    const heartIcon = document.querySelector('.heart-icon')
    heartIcon.classList.toggle('bi-heart')
    heartIcon.classList.toggle('bi-heart-fill')

    // 좋아요 갯수 변경
    const heartCnt = document.querySelector('.like-cnt')
    heartCnt.innerText = response.data.like_cnt
  })
})


// 댓글 수정 비동기 구현
// 1) 댓글 수정 버튼 클릭 시 댓글 수정 폼 생성
const commentUpdateBtns = document.querySelectorAll('.comment-update-btn')
console.log('어디야')
commentUpdateBtns.forEach((commentUpdateBtn) => {
  commentUpdateBtn.addEventListener('click', function (event) {
    event.preventDefault()
    console.log('왔니')
    // comment 수정 폼 불러오기
    const commentBlock = document.querySelector(`.comment-block-${commentUpdateBtn.dataset.fcommentPk}`)

    const commentUpdateForm = document.createElement('form')
    commentUpdateForm.classList.add('comment-update-complete-form')

    commentUpdateForm.setAttribute('data-free-pk', `${commentUpdateBtn.dataset.freePk}`)
    commentUpdateForm.setAttribute('data-comment-pk', `${commentUpdateBtn.dataset.fcommentPk}`)

    const content = document.querySelector(`.comment-${commentUpdateBtn.dataset.fcommentPk}-content`)

    commentUpdateForm.insertAdjacentHTML('beforeend', `
    <textarea name='content' rows='1' class='form-control' required>${content.innerText}</textarea>
    <input class=' my-3'  type='submit' value='OK'>
    `)

    commentBlock.append(commentUpdateForm)

    // 기존 comment 내용 지우기
    const commentContent = document.querySelector(`.comment-${commentUpdateBtn.dataset.fcommentPk}-content`)

    commentContent.remove()

    // 기존 삭제/수정 버튼 지우기
    const deleteBtn = document.querySelector(`.comment-block-${commentUpdateBtn.dataset.fcommentPk} input[type=submit]`)
    deleteBtn.remove()
    event.target.remove()

    // 2) 댓글 수정 폼을 제출할 때 content 반영
    const commentUpdateCompleteForm = document.querySelector('.comment-update-complete-form')

    commentUpdateCompleteForm.addEventListener('submit', function (event) {
      event.preventDefault()
      console.log(commentUpdateCompleteForm)
      axios({
        method: 'post',
        url: `/free/${commentUpdateCompleteForm.dataset.freePk}/comments/${commentUpdateCompleteForm.dataset.fcommentPk}/update/complete/`,
        data: new FormData(commentUpdateCompleteForm),
        headers: { 'X-CSRFToken': csrftoken },
      }).then((response) => {
        // comment 수정 폼 삭제
        commentUpdateCompleteForm.remove()

        // comment의 content 변경
        commentContent.innerText = response.data.comment_content
        const commentContentContainer = document.querySelector(`.comment-${commentUpdateBtn.dataset.fcommentPk}-content-container`)
        commentContentContainer.appendChild(commentContent)

        // 수정/삭제 버튼 생성
        commentBlock.append(deleteBtn)
      })
    })
  })
})