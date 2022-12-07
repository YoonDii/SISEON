//좋아요
const likeBtn = document.querySelector('#like-btn')
likeBtn.addEventListener('click', function (event) {
  axios({
    method: 'get',
    url: `/free/${event.target.dataset.likeId}/like/`
  })
    .then(response => {
      console.log(response.data)
      if (response.data.isLike === true) {
        event.target.classList.add('bi-heart-fill')
        event.target.classList.add('free-heart-fill')
        event.target.classList.remove('bi-heart')
        event.target.classList.remove('free-heart')
        // console.log('좋아요')
      } else {
        event.target.classList.add('bi-heart')
        event.target.classList.add('free-heart')
        event.target.classList.remove('bi-heart-fill')
        event.target.classList.remove('free-heart-fill')
        // console.log('좋아요아님')
      }
      const likeCount = document.querySelector('#likes')
      likeCount.innerHTML = `<p>${response.data.likeCount}</p>`
    })
})


//댓글 생성 비동기
const commentForm = document.querySelector('#comment-form')
const csrftoken = document
  .querySelector('[name=csrfmiddlewaretoken]')
  .value

commentForm
  .addEventListener('submit', function (event) {
    event.preventDefault();
    axios({
      method: 'post',
      url: `/free/${event.target.dataset.freeId}/comments_create/`,
      headers: {
        'X-CSRFToken': csrftoken
      },
      data: new FormData(commentForm)
    })
      .then(response => {
        console.log(response)
        const comment_count = document.querySelector('#comment_count')
        comment_count.innerHTML = `<p>댓글 ${response.data.comment_data_count}개</p>`
        const comments = document.querySelector('#comments')
        comments.textContent = "";
        const hr = document.createElement('hr')
        const comment_data = response.data.comment_data
        const user = response
          .data
          .user
        for (let i = 0; i < comment_data.length; i++) {
          const free_pk = response
            .data
            .free_pk
          console
            .log(comment_data[i].id, user, comment_data[i].unname)
          if (user === comment_data[i].id) {
            comments.insertAdjacentHTML('beforeend', `
                  <div class="comment-title">
                      <div class="user-date">
                        <!-- 작성자 -->
                        <p class="comment-user">${comment_data[i].userName}</p>
                        <!-- 작성일자 -->
                        <p class="date">${comment_data[i].updated_at}</p>
                      </div>

                      <div class="comment-buttons">
                        <!-- 댓글 수정창 -->
                        <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
                          <input id="input-${comment_data[i].commentPk}" type="text" value="${comment_data[i].content}">
                          <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-freeup-id="${free_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">확인</button>
                        </div>
 
                        <!-- 수정 버튼 -->
                        <button  onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-freeup-id="${free_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">수정</button>

                        <!-- 삭제 버튼 -->
                        <button  onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-freedel-id="${free_pk}" data-commentdel-id="${comment_data[i].commentPk}" class="delete-button">삭제</button>
                      </div> <!-- comment-buttons -->
                    </div> <!-- comment-title -->

                    <!-- 댓글 본문 -->
                    <p class="comment-contents">${comment_data[i].content}</p>
                    <hr class="comment-divider">
                  `);
          } else {
            comments.insertAdjacentHTML('beforeend', `
              <div class="comment-title">
                      <div class="user-date">
                        <!-- 작성자 -->
                        <p class="comment-user">${comment_data[i].userName}</p>
                        <!-- 작성일자 -->
                        <p class="date">${comment_data[i].updated_at}</p>
                      </div>
                    </div> <!-- comment-title -->

                    <!-- 댓글 본문 -->
                    <p class="comment-contents">${comment_data[i].content}</p>
                    <hr class="comment-divider">
                  `);
          }
        }
        commentForm
          .reset()
      })
      .catch(console.log(1))
  })


// 댓글 삭제 비동기
const delete_comment = (e) => {
  const comment_id = document
    .querySelector(`#${e.id}`)
    .id;
  axios({
    method: 'post',
    url: `/free/${event.target.dataset.freedelId}/comment_delete/${event.target.dataset.commentdelId}/delete/`,
    headers: {
      'X-CSRFToken': csrftoken
    }
  }).then(response => {
    console.log(response)
    if (response.data.comment_data_count === 0) {
      const comment_count = document.querySelector('#comment_count')
      comment_count.innerHTML = `<p>댓글 ${response.data.comment_data_count}개</p>
        <hr class="comment-start">
        <p id ="comment_empty" class="no-comment">등록된 댓글이 없습니다.<br>첫 댓글의 주인공이 되어보세요!</p>`
      const commentstart = document.querySelectorAll(".comment-start")
      commentstart[1].remove()
    }
    else {
      const comment_count = document.querySelector('#comment_count')
      comment_count.innerHTML = `<p>댓글 ${response.data.comment_data_count}개</p>`
    }
    const comments = document.querySelector('#comments')
    comments.textContent = "";
    const hr = document.createElement('hr')
    const comment_data = response.data.comment_data
    const user = response
      .data
      .user
    for (let i = 0; i < comment_data.length; i++) {
      const free_pk = response
        .data
        .free_pk
      console
        .log(comment_data[i].id, user, comment_data[i].unname)
      if (user === comment_data[i].id) {
        comments.insertAdjacentHTML('beforeend', `
          <div class="comment-title">
                      <div class="user-date">
                        <!-- 작성자 -->
                        <p class="comment-user">${comment_data[i].userName}</p>
                        <!-- 작성일자 -->
                        <p class="date">${comment_data[i].updated_at}</p>
                      </div>

                      <div class="comment-buttons">
                        <!-- 댓글 수정창 -->
                        <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
                          <input id="input-${comment_data[i].commentPk}" type="text" value="${comment_data[i].content}">
                          <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-freeup-id="${free_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">확인</button>
                        </div>
 
                        <!-- 수정 버튼 -->
                        <button  onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-freeup-id="${free_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">수정</button>

                        <!-- 삭제 버튼 -->
                        <button  onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-freedel-id="${free_pk}" data-commentdel-id="${comment_data[i].commentPk}" class="delete-button">삭제</button>
                      </div> <!-- comment-buttons -->
                    </div> <!-- comment-title -->

                    <!-- 댓글 본문 -->
                    <p class="comment-contents">${comment_data[i].content}</p>
                    <hr class="comment-divider">
            `);
      } else {
        comments.insertAdjacentHTML('beforeend', `
          <div class="comment-title">
                      <div class="user-date">
                        <!-- 작성자 -->
                        <p class="comment-user">${comment_data[i].userName}</p>
                        <!-- 작성일자 -->
                        <p class="date">${comment_data[i].updated_at}</p>
                      </div>
                    </div> <!-- comment-title -->

                    <!-- 댓글 본문 -->
                    <p class="comment-contents">${comment_data[i].content}</p>
                    <hr class="comment-divider">
            `);
      }
    }
    commentForm
      .reset()
  })
}


// 댓글 수정 비동기
const ok_function = (e) => {
  const commentId = event.target.dataset.commentupId
  const freeId = event.target.dataset.freeupId
  const inputCommentPk = document.querySelector(`#input-${commentId}`)

  axios({
    method: 'post',
    url: `/free/${event.target.dataset.freeupId}/comment_update/${event.target.dataset.commentupId}/update/`,
    headers: {
      'X-CSRFToken': csrftoken
    },
    data: {
      'content': inputCommentPk.value
    }
  }).then(response => {
    console.log(response)
    const comment_count = document.querySelector('#comment_count')
    comment_count.innerHTML = `<p>댓글 ${response.data.comment_data_count}개</p>`
    const comments = document.querySelector('#comments')
    comments.textContent = "";
    const hr = document.createElement('hr')
    const comment_data = response.data.comment_data
    const user = response
      .data
      .user
    for (let i = 0; i < comment_data.length; i++) {
      const free_pk = response
        .data
        .free_pk
      console
        .log(comment_data[i].id, user, comment_data[i].unname)
      if (user === comment_data[i].id) {
        comments.insertAdjacentHTML('beforeend', `
          <div class="comment-title">
                      <div class="user-date">
                        <!-- 작성자 -->
                        <p class="comment-user">${comment_data[i].userName}</p>
                        <!-- 작성일자 -->
                        <p class="date">${comment_data[i].updated_at}</p>
                      </div>

                      <div class="comment-buttons">
                        <!-- 댓글 수정창 -->
                        <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
                          <input id="input-${comment_data[i].commentPk}" type="text" value="${comment_data[i].content}">
                          <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-freeup-id="${free_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">확인</button>
                        </div>
 
                        <!-- 수정 버튼 -->
                        <button  onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-freeup-id="${free_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">수정</button>

                        <!-- 삭제 버튼 -->
                        <button  onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-freedel-id="${free_pk}" data-commentdel-id="${comment_data[i].commentPk}" class="delete-button">삭제</button>
                      </div> <!-- comment-buttons -->
                    </div> <!-- comment-title -->

                    <!-- 댓글 본문 -->
                    <p class="comment-contents">${comment_data[i].content}</p>
                    <hr class="comment-divider">
            `);
      } else {
        comments.insertAdjacentHTML('beforeend', `
          <div class="comment-title">
                      <div class="user-date">
                        <!-- 작성자 -->
                        <p class="comment-user">${comment_data[i].userName}</p>
                        <!-- 작성일자 -->
                        <p class="date">${comment_data[i].updated_at}</p>
                      </div>
                    </div> <!-- comment-title -->

                    <!-- 댓글 본문 -->
                    <p class="comment-contents">${comment_data[i].content}</p>
                    <hr class="comment-divider">
            `);
      }
    }
    commentForm
      .reset()
  })
}
const update_comment = (e) => {
  const comment_id = document
    .querySelector(`#${e.id}`)
    .id
  const input = document.createElement('input')
  const comment = document.querySelector('#comment')
  const span = document.createElement('span')
  const comment_update_form = document.querySelector(`#form-${e.id}`)
  const comment_update = document.querySelector(`#${e.id}`)
  comment_update_form.style.display = ""
  comment_update.style.display = "none"
}

