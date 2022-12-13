//메시지

window.setTimeout(function() {
  $(".alert-auto-dismissible").fadeTo(2000, 500).slideUp(500, function(){
    $(".alert-auto-dismissible").alert('close');
  });
}, 4000);

//좋아요
const likeBtn = document.querySelector('#like-btn')
likeBtn.addEventListener('click', function (event) {
  axios({
    method: 'get',
    url: `/gathering/${event.target.dataset.likeId}/like/`
  })
    .then(response => {
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
      likeCount.innerHTML = `${response.data.like_cnt}`
    })
})

  //댓글생성
  const commentForm = document.querySelector('#comment-form')
  const csrftoken = document
    .querySelector('[name=csrfmiddlewaretoken]')
    .value

    commentForm
    .addEventListener('submit', function (event) {
      event.preventDefault();
      axios({
        method: 'post',
        url: `/gathering/${event.target.dataset.gatheringId}/comments_create/`,
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
          const recomment_data = response.data.recomment_data2
          const user = response.data.user
          for (let i = 0; i < comment_data.length; i++) {
            const gathering_pk = response.data.gathering_pk
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
                  <!-- 수정 버튼 -->
                  <button onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">수정</button>
  
                  <!-- 삭제 버튼 -->
                  <button onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-gatheringdel-id="${gathering_pk}" data-commentdel-id="${comment_data[i].commentPk}" class="delete-button">삭제</button>
                </div> <!-- comment-buttons -->
              </div> <!-- comment-title -->
  
  
              <!-- 댓글 수정창 -->
              <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
                <textarea name="content"  cols="10" rows="1" class="form-control" placeholder="" required="" id="input-${comment_data[i].commentPk}">${comment_data[i].content}</textarea>
                <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="update-button">확인</button>
              </div>
  
  
              <!-- 댓글 본문 -->
              <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
              
  
              <!-- 답글 버튼 -->
              <div class="button-count">
                <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
                <p class="comment-count">${comment_data[i].recomment_cnt}</p>
              </div>
  
              <!-- 답글창 -->
              <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
                <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                  <div class="mb-3">
                    <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                  </div>
                </form>
  
                <!-- 답글 등록 버튼 -->
                <div class="sb-div">
                  <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
                </div>
              </div> <!-- recomment-form -->
  
              <!-- 답글 내용 -->
              <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
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
              <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
              
  
  
              <!-- 답글 버튼 -->
              <div class="button-count">
                <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
                <p class="comment-count">${comment_data[i].recomment_cnt}</p>
              </div>
  
              <!-- 답글창 -->
              <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
                <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                  <div class="mb-3">
                    <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                  </div>
                </form>
  
                <!-- 답글 등록 버튼 -->
                <div class="sb-div">
                  <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
                </div>
              </div> <!-- recomment-form -->
  
              <!-- 답글 내용 -->
              <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
              <hr class="comment-divider">
              `);
            }
          }
  
          for (let j = 0; j < recomment_data.length; j++) {
            const gathering_pk = response.data.gathering_pk
            if (user === recomment_data[j].id) {
              const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
              re.insertAdjacentHTML('beforeend', `
            <!-- 닉네임, 답글 내용, 삭제 버튼 -->
              <!-- 닉네임, 답글 내용, 삭제 버튼 -->
              <div class="user-delete">
                <p class="comment-user">${recomment_data[j].userName}</p>
                <button onclick="redelete_comment(this)" id="recomment-delete-${recomment_data[j].recommentPk}" data-recommentdel-id="${recomment_data[j].recommentPk}" data-recommentparentdel-id="${recomment_data[j].commentPk}" data-gatheringredel-id="${gathering_pk}" class="delete-button">삭제</button>
              </div>
              <p class="comment-contents">${recomment_data[j].content}</p>
            `)
            } else {
              const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
              re.insertAdjacentHTML('beforeend', `
              <p class="comment-user">${recomment_data[j].userName}</p>
              <p class="comment-contents">${recomment_data[j].content}</p>
            `)
            }
          }
          commentForm.reset()
        })
    })


  // 댓글 삭제 비동기
  const delete_comment = (e) => {
    const comment_id = document
      .querySelector(`#${e.id}`)
      .id;
    axios({
      method: 'post',
      url: `/gathering/${event.target.dataset.gatheringdelId}/comment_delete/${event.target.dataset.commentdelId}/delete/`,
      headers: {
        'X-CSRFToken': csrftoken
      }
    })
      .then(response => {
        console.log(response)
        if (response.data.comment_data_count === 0) {
          const comment_count = document.querySelector('#comment_count')
          comment_count.innerHTML = `<p>댓글 ${response.data.comment_data_count}개</p>
        <hr class="comment-start">
        <p id ="comment_empty" class="no-comment">등록된 댓글이 없습니다.<br>첫 댓글의 주인공이 되어보세요!</p>`
          const commentstart = document.querySelectorAll(".comment-start")
          console.log(commentstart)
          if (commentstart[1]) {
            commentstart[1].remove()
          }
        } else {
          const comment_count = document.querySelector('#comment_count')
          comment_count.innerHTML = `<p>댓글 ${response.data.comment_data_count}개</p>`
        }
        const comments = document.querySelector('#comments')
        comments.textContent = "";
        const hr = document.createElement('hr')
        const comment_data = response.data.comment_data
        const recomment_data = response.data.recomment_data2
        const user = response.data.user
        for (let i = 0; i < comment_data.length; i++) {
          const gathering_pk = response.data.gathering_pk
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
                <!-- 수정 버튼 -->
                <button onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">수정</button>

                <!-- 삭제 버튼 -->
                <button onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-gatheringdel-id="${gathering_pk}" data-commentdel-id="${comment_data[i].commentPk}" class="delete-button">삭제</button>
              </div> <!-- comment-buttons -->
            </div> <!-- comment-title -->


            <!-- 댓글 수정창 -->
            <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
              <textarea name="content"  cols="10" rows="1" class="form-control" placeholder="" required="" id="input-${comment_data[i].commentPk}">${comment_data[i].content}</textarea>
              <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="update-button">확인</button>
            </div>


            <!-- 댓글 본문 -->
            <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
            

            <!-- 답글 버튼 -->
            <div class="button-count">
              <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
              <p class="comment-count">${comment_data[i].recomment_cnt}</p>
            </div>

            <!-- 답글창 -->
            <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
              <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                <div class="mb-3">
                  <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                </div>
              </form>

              <!-- 답글 등록 버튼 -->
              <div class="sb-div">
                <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
              </div>
            </div> <!-- recomment-form -->

            <!-- 답글 내용 -->
            <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
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
            <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
            


            <!-- 답글 버튼 -->
            <div class="button-count">
              <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
              <p class="comment-count">${comment_data[i].recomment_cnt}</p>
            </div>

            <!-- 답글창 -->
            <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
              <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                <div class="mb-3">
                  <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                </div>
              </form>

              <!-- 답글 등록 버튼 -->
              <div class="sb-div">
                <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
              </div>
            </div> <!-- recomment-form -->

            <!-- 답글 내용 -->
            <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
            <hr class="comment-divider">
            `);
          }
        }

        for (let j = 0; j < recomment_data.length; j++) {
          const gathering_pk = response.data.gathering_pk
          if (user === recomment_data[j].id) {
            const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
            re.insertAdjacentHTML('beforeend', `
          <!-- 닉네임, 답글 내용, 삭제 버튼 -->
            <!-- 닉네임, 답글 내용, 삭제 버튼 -->
            <div class="user-delete">
              <p class="comment-user">${recomment_data[j].userName}</p>
              <button onclick="redelete_comment(this)" id="recomment-delete-${recomment_data[j].recommentPk}" data-recommentdel-id="${recomment_data[j].recommentPk}" data-recommentparentdel-id="${recomment_data[j].commentPk}" data-gatheringredel-id="${gathering_pk}" class="delete-button">삭제</button>
            </div>
            <p class="comment-contents">${recomment_data[j].content}</p>
          `)
          } else {
            const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
            re.insertAdjacentHTML('beforeend', `
            <p class="comment-user">${recomment_data[j].userName}</p>
            <p class="comment-contents">${recomment_data[j].content}</p>
          `)
          }
        }
        commentForm.reset()
      })
  }


  // 댓글 수정 비동기
  const ok_function = (e) => {
    const commentId = event.target.dataset.commentupId
    const gatheringId = event.target.dataset.gatheringupId
    const inputCommentPk = document.querySelector(`#input-${commentId}`)

    axios({
      method: 'post',
      url: `/gathering/${event.target.dataset.gatheringupId}/comment_update/${event.target.dataset.commentupId}/update/`,
      headers: {
        'X-CSRFToken': csrftoken
      },
      data: {
        'content': inputCommentPk.value
      }
    })
      .then(response => {
        console.log(response)
        const comment_count = document.querySelector('#comment_count')

        const comments = document.querySelector('#comments')
        comments.textContent = "";
        const hr = document.createElement('hr')
        const comment_data = response.data.comment_data
        const recomment_data = response.data.recomment_data2
        const user = response.data.user
        for (let i = 0; i < comment_data.length; i++) {
          const gathering_pk = response.data.gathering_pk
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
                <!-- 수정 버튼 -->
                <button onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">수정</button>

                <!-- 삭제 버튼 -->
                <button onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-gatheringdel-id="${gathering_pk}" data-commentdel-id="${comment_data[i].commentPk}" class="delete-button">삭제</button>
              </div> <!-- comment-buttons -->
            </div> <!-- comment-title -->


            <!-- 댓글 수정창 -->
            <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
              <textarea name="content"  cols="10" rows="1" class="form-control" placeholder="" required="" id="input-${comment_data[i].commentPk}">${comment_data[i].content}</textarea>
              <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="update-button">확인</button>
            </div>


            <!-- 댓글 본문 -->
            <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
            

            <!-- 답글 버튼 -->
            <div class="button-count">
              <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
              <p class="comment-count">${comment_data[i].recomment_cnt}</p>
            </div>

            <!-- 답글창 -->
            <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
              <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                <div class="mb-3">
                  <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                </div>
              </form>

              <!-- 답글 등록 버튼 -->
              <div class="sb-div">
                <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
              </div>
            </div> <!-- recomment-form -->

            <!-- 답글 내용 -->
            <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
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
            <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
            


            <!-- 답글 버튼 -->
            <div class="button-count">
              <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
              <p class="comment-count">${comment_data[i].recomment_cnt}</p>
            </div>

            <!-- 답글창 -->
            <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
              <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                <div class="mb-3">
                  <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                </div>
              </form>

              <!-- 답글 등록 버튼 -->
              <div class="sb-div">
                <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
              </div>
            </div> <!-- recomment-form -->

            <!-- 답글 내용 -->
            <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
            <hr class="comment-divider">
            `);
          }
        }

        for (let j = 0; j < recomment_data.length; j++) {
          const gathering_pk = response.data.gathering_pk
          if (user === recomment_data[j].id) {
            const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
            re.insertAdjacentHTML('beforeend', `
          <!-- 닉네임, 답글 내용, 삭제 버튼 -->
            <!-- 닉네임, 답글 내용, 삭제 버튼 -->
            <div class="user-delete">
              <p class="comment-user">${recomment_data[j].userName}</p>
              <button onclick="redelete_comment(this)" id="recomment-delete-${recomment_data[j].recommentPk}" data-recommentdel-id="${recomment_data[j].recommentPk}" data-recommentparentdel-id="${recomment_data[j].commentPk}" data-gatheringredel-id="${gathering_pk}" class="delete-button">삭제</button>
            </div>
            <p class="comment-contents">${recomment_data[j].content}</p>
          `)
          } else {
            const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
            re.insertAdjacentHTML('beforeend', `
            <p class="comment-user">${recomment_data[j].userName}</p>
            <p class="comment-contents">${recomment_data[j].content}</p>
          `)
          }
        }
        commentForm.reset()
      })
  }
  const update_comment = (e) => {
    const comment_id = document
      .querySelector(`#${e.id}`)
      .id
    const input = document.createElement('input')
    const comment = document.querySelector('#comment')
    const span = document.createElement('span')
    const p = document.querySelector(`#comment-contents-${event.target.dataset.commentupId}`)
    p.remove()
    const comment_update_form = document.querySelector(`#form-${e.id}`)
    const comment_update = document.querySelector(`#${e.id}`)
    comment_update_form.style.display = ""
    comment_update.style.display = "none"
  }


  //대댓글 삭제
  const redelete_comment = (e) => {
    const comment_id = document
      .querySelector(`#${e.id}`)
      .id;
    const gatheringId = event.target.dataset.gatheringredelId
    const commentId = event.target.dataset.recommentparentdelId
    const recommentId = event
      .target
      .dataset
      .recommentdelId
      axios({
        method: 'post',
        url: `/gathering/${gatheringId}/recomment_delete/${commentId}/delete/${recommentId}/`,
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
      .then(response => {
        console.log(response)
        const comments = document.querySelector('#comments')
        comments.textContent = "";
        const hr = document.createElement('hr')
        const comment_data = response.data.comment_data
        const recomment_data = response.data.recomment_data2
        const user = response.data.user
        for (let i = 0; i < comment_data.length; i++) {
          const gathering_pk = response.data.gathering_pk
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
                <!-- 수정 버튼 -->
                <button onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">수정</button>

                <!-- 삭제 버튼 -->
                <button onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-gatheringdel-id="${gathering_pk}" data-commentdel-id="${comment_data[i].commentPk}" class="delete-button">삭제</button>
              </div> <!-- comment-buttons -->
            </div> <!-- comment-title -->


            <!-- 댓글 수정창 -->
            <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
              <textarea name="content"  cols="10" rows="1" class="form-control" placeholder="" required="" id="input-${comment_data[i].commentPk}">${comment_data[i].content}</textarea>
              <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="update-button">확인</button>
            </div>


            <!-- 댓글 본문 -->
            <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
            

            <!-- 답글 버튼 -->
            <div class="button-count">
              <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
              <p class="comment-count">${comment_data[i].recomment_cnt}</p>
            </div>

            <!-- 답글창 -->
            <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
              <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                <div class="mb-3">
                  <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                </div>
              </form>

              <!-- 답글 등록 버튼 -->
              <div class="sb-div">
                <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
              </div>
            </div> <!-- recomment-form -->

            <!-- 답글 내용 -->
            <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
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
            <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
            


            <!-- 답글 버튼 -->
            <div class="button-count">
              <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
              <p class="comment-count">${comment_data[i].recomment_cnt}</p>
            </div>

            <!-- 답글창 -->
            <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
              <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                <div class="mb-3">
                  <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                </div>
              </form>

              <!-- 답글 등록 버튼 -->
              <div class="sb-div">
                <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
              </div>
            </div> <!-- recomment-form -->

            <!-- 답글 내용 -->
            <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
            <hr class="comment-divider">
            `);
          }
        }

        for (let j = 0; j < recomment_data.length; j++) {
          const gathering_pk = response.data.gathering_pk
          if (user === recomment_data[j].id) {
            const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
            re.insertAdjacentHTML('beforeend', `
          <!-- 닉네임, 답글 내용, 삭제 버튼 -->
            <!-- 닉네임, 답글 내용, 삭제 버튼 -->
            <div class="user-delete">
              <p class="comment-user">${recomment_data[j].userName}</p>
              <button onclick="redelete_comment(this)" id="recomment-delete-${recomment_data[j].recommentPk}" data-recommentdel-id="${recomment_data[j].recommentPk}" data-recommentparentdel-id="${recomment_data[j].commentPk}" data-gatheringredel-id="${gathering_pk}" class="delete-button">삭제</button>
            </div>
            <p class="comment-contents">${recomment_data[j].content}</p>
          `)
          } else {
            const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
            re.insertAdjacentHTML('beforeend', `
            <p class="comment-user">${recomment_data[j].userName}</p>
            <p class="comment-contents">${recomment_data[j].content}</p>
          `)
          }
        }
        commentForm.reset()
      })
  }


  //대댓글 생성
  const recomment_create_comment = (e) => {
    const recomment_id = document
      .querySelector(`#${e.id}`)
      .id
    const comment = document.querySelector('#comment')
    const new_recomment_create = document.querySelector(`#form-${e.id}`)
    const comment_update = document.querySelector(`#${e.id}`)
    new_recomment_create.style.display = ""
    comment_update.style.display = "none"
  }
  const answer = (e) => {
    const commentId = event.target.dataset.commentrecId
    const reviewId = event.target.dataset.gatheringrecId
    const recommentForm = document.querySelector(`#recomment-form-${commentId}`)
    const csrftoken = document
      .querySelector('[name=csrfmiddlewaretoken]')
      .value
      axios({
        method: 'post',
        url: `/gathering/${event.target.dataset.gatheringrecId}/recomment_create/${event.target.dataset.commentrecId}/`,
        headers: {
          'X-CSRFToken': csrftoken
        },
        data: new FormData(recommentForm)
      })
      .then(response => {
        console.log(response)
        const comment_count = document.querySelector('#comment_count')
        comment_count.innerHTML = `<p>댓글 ${response.data.comment_data_count}개</p>`
        const comments = document.querySelector('#comments')
        comments.textContent = "";
        const hr = document.createElement('hr')
        const comment_data = response.data.comment_data
        const recomment_data = response.data.recomment_data2
        const user = response.data.user
        for (let i = 0; i < comment_data.length; i++) {
          const gathering_pk = response.data.gathering_pk
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
                <!-- 수정 버튼 -->
                <button onclick="update_comment(this)" id="comment-update-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="edit-button">수정</button>

                <!-- 삭제 버튼 -->
                <button onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-gatheringdel-id="${gathering_pk}" data-commentdel-id="${comment_data[i].commentPk}" class="delete-button">삭제</button>
              </div> <!-- comment-buttons -->
            </div> <!-- comment-title -->


            <!-- 댓글 수정창 -->
            <div id="form-comment-update-${comment_data[i].commentPk}" style="display:none;">
              <textarea name="content"  cols="10" rows="1" class="form-control" placeholder="" required="" id="input-${comment_data[i].commentPk}">${comment_data[i].content}</textarea>
              <button onclick="ok_function(this)" id="okBtn-${comment_data[i].commentPk}" data-gatheringup-id="${gathering_pk}" data-commentup-id="${comment_data[i].commentPk}" class="update-button">확인</button>
            </div>


            <!-- 댓글 본문 -->
            <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
            

            <!-- 답글 버튼 -->
            <div class="button-count">
              <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
              <p class="comment-count">${comment_data[i].recomment_cnt}</p>
            </div>

            <!-- 답글창 -->
            <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
              <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                <div class="mb-3">
                  <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                </div>
              </form>

              <!-- 답글 등록 버튼 -->
              <div class="sb-div">
                <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
              </div>
            </div> <!-- recomment-form -->

            <!-- 답글 내용 -->
            <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
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
            <p id="comment-contents-${comment_data[i].commentPk}" class="comment-contents">${comment_data[i].content}</p>
            


            <!-- 답글 버튼 -->
            <div class="button-count">
              <button onclick="recomment_create_comment(this)" id='recomment-create-${comment_data[i].commentPk}' data-gatheringrec-id="${gathering_pk}" data-recommentcre-id="${comment_data[i].commentPk}" class="recomment-button">답글</button>
              <p class="comment-count">${comment_data[i].recomment_cnt}</p>
            </div>

            <!-- 답글창 -->
            <div id='form-recomment-create-${comment_data[i].commentPk}' class="recomment-form" style='display:none;'>
              <form id="recomment-form-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}">
                <div class="mb-3">
                  <textarea name="body" cols="40" rows="1" class="form-control" maxlength="200" placeholder="답글을 남겨보세요!\n답글이 길어질 땐 답글창을 늘려보세요." required="" id="id_body"></textarea>
                </div>
              </form>

              <!-- 답글 등록 버튼 -->
              <div class="sb-div">
                <button onclick="answer(this)" id="answer-${comment_data[i].commentPk}" data-gatheringrec-id="${gathering_pk}" data-commentrec-id="${comment_data[i].commentPk}" class="recomment-submit-button">등록</button>
              </div>
            </div> <!-- recomment-form -->

            <!-- 답글 내용 -->
            <div id="re-${comment_data[i].commentPk}" class="recomments"></div>
            <hr class="comment-divider">
            `);
          }
        }

        for (let j = 0; j < recomment_data.length; j++) {
          const gathering_pk = response.data.gathering_pk
          if (user === recomment_data[j].id) {
            const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
            re.insertAdjacentHTML('beforeend', `
          <!-- 닉네임, 답글 내용, 삭제 버튼 -->
            <!-- 닉네임, 답글 내용, 삭제 버튼 -->
            <div class="user-delete">
              <p class="comment-user">${recomment_data[j].userName}</p>
              <button onclick="redelete_comment(this)" id="recomment-delete-${recomment_data[j].recommentPk}" data-recommentdel-id="${recomment_data[j].recommentPk}" data-recommentparentdel-id="${recomment_data[j].commentPk}" data-gatheringredel-id="${gathering_pk}" class="delete-button">삭제</button>
            </div>
            <p class="comment-contents">${recomment_data[j].content}</p>
          `)
          } else {
            const re = document.querySelector(`#re-${recomment_data[j].commentPk}`)
            re.insertAdjacentHTML('beforeend', `
            <p class="comment-user">${recomment_data[j].userName}</p>
            <p class="comment-contents">${recomment_data[j].content}</p>
          `)
          }
        }
        commentForm.reset()
      })
  }
document.querySelector("#result").addEventListener('click', function(e) {
  const resultModal = document.querySelector("#resultModal")
  resultModal.setAttribute('class', 'modal fade show')
  resultModal.setAttribute('role', 'dialog')
  resultModal.classList.add("modal-bodys")
  
  modaldialog =  document.querySelector(".modal-dialog")

  modaldialog.classList.add("modal-dialog")

  resultModal.classList.remove('option-inactive')
  resultModal.classList.add('option-active')

  console.log(resultModal)
})

document.querySelector("#close").addEventListener('click', function(e){
  const resultModal = document.querySelector("#resultModal")

  resultModal.classList.add('option-inactive')
  resultModal.classList.remove('option-active')

  resultModal.classList.remove("modal-bodys")
})

document.querySelector(".btn-close").addEventListener('click', function(e){
  const resultModal = document.querySelector("#resultModal")

  resultModal.classList.add('option-inactive')
  resultModal.classList.remove('option-active')

  resultModal.classList.remove("modal-bodys")
})