//좋아요
  const likeBtn = document.querySelector('#like-btn')
  likeBtn.addEventListener('click', function (event) {
  console.log(event.target.dataset)
  axios({
    method: 'get',
    url: `/articles/${event.target.dataset.likeId}/like/`
  })
  .then(response => {
    console.log(response.data)
    if (response.data.isLike === true) {
      event.target.classList.add('bi-heart-fill')
      event.target.classList.add('article-heart-fill')
      event.target.classList.remove('bi-heart')
      event.target.classList.remove('article-heart')
      // console.log('좋아요')
    } else {
      event.target.classList.add('bi-heart')
      event.target.classList.add('article-heart')
      event.target.classList.remove('bi-heart-fill')
      event.target.classList.remove('article-heart-fill')
      // console.log('좋아요아님')
    }
    const likeCount = document.querySelector('#likes')
    likeCount.innerHTML = `<h6 class="likes m-0"> ${response.data.likeCount}</h6>`
  })
})


  //댓글 생성 비동기
  const commentForm = document.querySelector('#comment-form')
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

      commentForm.addEventListener('submit', function (event) {
        event.preventDefault();
        axios({
          method: 'post',
          url: `/articles/${event.target.dataset.articlesId}/comment_create/`,
          headers: {
            'X-CSRFToken': csrftoken
          },
          data: new FormData(commentForm)
        })
          .then(response => {
            console.log(response)
            const comments = document.querySelector('#comments')
            comments.textContent = "";
            const hr = document.createElement('hr')
            const comment_data = response.data.comment_data
            const user = response.data.user
              for (let i = 0; i < comment_data.length; i++) {
                const articles_pk = response.data.articles_pk
                  console.log(comment_data[i].id, user, comment_data[i].unname)
                if (user === comment_data[i].id) {
                  comments.insertAdjacentHTML('beforeend', `
                  <div class="comment">
                    <h4>${comment_data[i].userName} - ${comment_data[i].content}</h4>
                    <div>
                      <div>
                        <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
                          <input id="input-${comment_data[i].commentPk}" type="text" value="${comment_data[i].content}">
                          <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-articlesup-id="${ articles_pk }" data-commentup-id="${comment_data[i].commentPk}">확인</button>
                        </div>
                        <button  onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-articlesup-id="${ articles_pk }" data-commentup-id="${comment_data[i].commentPk}">수정</button>\
                        <button  onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-articlesdel-id="${ articles_pk }" data-commentdel-id="${comment_data[i].commentPk}">삭제</button>
                      </div>
                    </div>
                  </div>
                  `);
                } else {
                  comments.insertAdjacentHTML('beforeend', `
                    <div class="comment">
                      <h4>${comment_data[i].userName} - ${comment_data[i].content}</h4>
                    </div>
                  `);
                }
              }
              commentForm
              .reset()
          }
          )
          .catch(console.log(1))
        })


  // 댓글 삭제 비동기
  const delete_comment = (e) => {
    const comment_id = document
      .querySelector(`#${e.id}`)
      .id;
    axios({
      method: 'post',
      url: `/articles/${event.target.dataset.articlesdelId}/comment_delete/${event.target.dataset.commentdelId}/delete/`,
      headers: {
        'X-CSRFToken': csrftoken
      }
    }).then(response => {
      console.log(response)
      const comments = document.querySelector('#comments')
      comments.textContent = "";
      const hr = document.createElement('hr')
      const comment_data = response.data.comment_data
      const user = response.data.user
        for (let i = 0; i < comment_data.length; i++) {
          const articles_pk = response.data.articles_pk
            console.log(comment_data[i].id, user, comment_data[i].unname)
          if (user === comment_data[i].id) {
            comments.insertAdjacentHTML('beforeend', `
            <div class="comment">
              <h4>${comment_data[i].userName} - ${comment_data[i].content}</h4>
              <div>
                <div>
                  <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
                    <input id="input-${comment_data[i].commentPk}" type="text" value="${comment_data[i].content}">
                    <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-articlesup-id="${ articles_pk }" data-commentup-id="${comment_data[i].commentPk}">확인</button>
                  </div>
                  <button  onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-articlesup-id="${ articles_pk }" data-commentup-id="${comment_data[i].commentPk}">수정</button>\
                  <button  onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-articlesdel-id="${ articles_pk }" data-commentdel-id="${comment_data[i].commentPk}">삭제</button>
                </div>
              </div>
            </div>
            `);
          } else {
            comments.insertAdjacentHTML('beforeend', `
              <div class="comment">
                <h4>${comment_data[i].userName} - ${comment_data[i].content}</h4>
              </div>
            `);
          }
        }
        commentForm
        .reset()
      }
    )
  }


  // 댓글 수정 비동기
  const ok_function = (e) => {
    const commentId = event.target.dataset.commentupId
    const reviewId = event.target.dataset.reviewupId
    const inputCommentPk = document.querySelector(`#input-${commentId}`)

    axios({
      method: 'post',
      url: `/articles/${event.target.dataset.articlesupId}/comment_update/${event.target.dataset.commentupId}/update/`,
      headers: {
        'X-CSRFToken': csrftoken
      },
      data: {
        'content': inputCommentPk.value
      }
    }).then(response => {
      console.log(response)
      const comments = document.querySelector('#comments')
      comments.textContent = "";
      const hr = document.createElement('hr')
      const comment_data = response.data.comment_data
      const user = response.data.user
        for (let i = 0; i < comment_data.length; i++) {
          const articles_pk = response.data.articles_pk
            console.log(comment_data[i].id, user, comment_data[i].unname)
          if (user === comment_data[i].id) {
            comments.insertAdjacentHTML('beforeend', `
            <div class="comment">
              <h4>${comment_data[i].userName} - ${comment_data[i].content}</h4>
              <div>
                <div>
                  <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
                    <input id="input-${comment_data[i].commentPk}" type="text" value="${comment_data[i].content}">
                    <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-articlesup-id="${ articles_pk }" data-commentup-id="${comment_data[i].commentPk}">확인</button>
                  </div>
                  <button  onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-articlesup-id="${ articles_pk }" data-commentup-id="${comment_data[i].commentPk}">수정</button>\
                  <button  onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-articlesdel-id="${ articles_pk }" data-commentdel-id="${comment_data[i].commentPk}">삭제</button>
                </div>
              </div>
            </div>
            `);
          } else {
            comments.insertAdjacentHTML('beforeend', `
              <div class="comment">
                <h4>${comment_data[i].userName} - ${comment_data[i].content}</h4>
              </div>
            `);
          }
        }
        commentForm
        .reset()
      }
    )
  }
  const update_comment = (e) => {
    const comment_id = document.querySelector(`#${e.id}`).id
    const input = document.createElement('input')
    const comment = document.querySelector('#comment')
    const span = document.createElement('span')
    const comment_update_form = document.querySelector(`#form-${e.id}`)
    const comment_update = document.querySelector(`#${e.id}`)
    comment_update_form.style.display = ""
    comment_update.style.display = "none"
  }

