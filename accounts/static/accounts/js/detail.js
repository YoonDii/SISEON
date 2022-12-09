//프로필 카테고리
$(document).ready(function () {
  // 탭을 클릭하면
  $('ul.tabs li').click(function () {
    // 그 탭의 data-tab을 들고옴
    var tab_id = $(this).attr('data-tab');
    // 모든 탭의 li와 div를 제거함
    $('ul.tabs li').removeClass('current');
    $('.tab-content').removeClass('current');
    //클릭한 탭의 클래스, id에 current를 더함
    $(this).addClass('current');
    $("#" + tab_id).addClass('current');
  })

})
document.querySelector('.down').addEventListener('click', function (e) {
  const option_value = e.target.value
  const articles = document.querySelector('#my-articles')
  const frees = document.querySelector('#my-frees')
  const gatherings = document.querySelector('#my-gatherings')
  // 전체
  if (option_value == 0) {
    articles.setAttribute('class', 'option-active')
    frees.setAttribute('class', 'option-active')
    gatherings.setAttribute('class', 'option-active')
  }
  // 질문
  else if (option_value == 1) {
    articles.setAttribute('class', 'option-active')
    frees.setAttribute('class', 'option-inactive')
    gatherings.setAttribute('class', 'option-inactive')
  }
  // 자유
  else if (option_value == 2) {
    articles.setAttribute('class', 'option-inactive')
    frees.setAttribute('class', 'option-active')
    gatherings.setAttribute('class', 'option-inactive')
  }
  //모임
  else {
    articles.setAttribute('class', 'option-inactive')
    frees.setAttribute('class', 'option-inactive')
    gatherings.setAttribute('class', 'option-active')
  }
})
document.querySelector('.down1').addEventListener('click', function (e) {
  const option_value = e.target.value
  const articlescomment = document.querySelector('#my-articles-comment')
  const freescomment = document.querySelector('#my-frees-comment')
  const gatheringscomment = document.querySelector('#my-gatherings-comment')
  // 전체
  if (option_value == 4) {
    articlescomment.setAttribute('class', 'option-active')
    freescomment.setAttribute('class', 'option-active')
    gatheringscomment.setAttribute('class', 'option-active')
  }
  // 질문
  else if (option_value == 5) {
    articlescomment.setAttribute('class', 'option-active')
    freescomment.setAttribute('class', 'option-inactive')
    gatheringscomment.setAttribute('class', 'option-inactive')
  }
  // 자유
  else if (option_value == 6){
    articlescomment.setAttribute('class', 'option-inactive')
    freescomment.setAttribute('class', 'option-active')
    gatheringscomment.setAttribute('class', 'option-inactive')
  }
  // 모임
  else {
    articlescomment.setAttribute('class', 'option-inactive')
    freescomment.setAttribute('class', 'option-inactive')
    gatheringscomment.setAttribute('class', 'option-active')
  }
})
document.querySelector('.down2').addEventListener('click', function (e) {
  const option_value = e.target.value
  const mytonotes = document.querySelector('#my-to-notes')
  const myfromnotes = document.querySelector('#my-from-notes')
  // 전체
  if (option_value == 8) {
    mytonotes.setAttribute('class', 'option-active')
    myfromnotes.setAttribute('class', 'option-active')
  }
  // 보낸
  else if (option_value == 9) {
    mytonotes.setAttribute('class', 'option-active')
    myfromnotes.setAttribute('class', 'option-inactive')
  }
  // 받은
  else {
    mytonotes.setAttribute('class', 'option-inactive')
    myfromnotes.setAttribute('class', 'option-active')
  }
})
// 팔로우 기능
const followBtn = document.querySelector('#follow-btn')

// 버튼을 클릭하면
followBtn.addEventListener('click', function (event) {
  // 팔로우 할 유저 아이디를 불러옴
  axios({
    method: 'get',
    url: `/accounts/${event.target.dataset.userId}/follow/`
  })
    .then(response => {
      // 응답 데이터를 출력함
      // 만약에 팔로우 상태일 경우
      console.log(response)
      if (response.data.is_followed === true) {
        // 팔로우 취소 버튼을 위임하고
        event.target.classList.add('unfollow-button')
        followBtn.innerText = '팔로우 취소'
        // 팔로우 버튼을 없앰
        event.target.classList.remove('follow-button')
        // 팔로우 상태가 아닐 경우
      } else {
        // 팔로우 버튼을 위임하고
        event.target.classList.add('follow-button')
        followBtn.innerText = '팔로우'
        // 팔로우 취소 버튼을 없앰
        event.target.classList.remove('unfollow-button')
      }

      // 팔로우 숫자 변수 설정하고
      const followCnt = document.querySelector('#follow-cnt')
      const followersCountTag = document.querySelector('.followers-count')
      const followingsCountTag = document.querySelector('.followings-count')
      const followersCount = response.data.followers_count
      const followingsCount = response.data.followings_count
      followersCountTag.innerText = followersCount
      followingsCountTag.innerText = followingsCount

      const followersmodel = document.querySelector("#followers-modal")
      const followingsmodel = document.querySelector("#followings-modal")

      const f_datas = response.data.f_datas
      let modal_content = ''
      for(let i = 0; i < f_datas.length; i++) {
        console.log(f_datas.length)
        console.log(f_datas[i])
        console.log('=========')
        modal_content += `<div class="follow-user">`
        modal_content += `<a href="/accounts/${f_datas[i].follower_pk}/detail/">`
        let profile_src = ''
        if (f_datas[i].image) {
          profile_src = `${f_datas[i].follower_img}`;
        }
        else {
          profile_src = `{% static 'images/logo_png.png' %}`;
        }
        
        modal_content += `<img class='follow-profile-img' src=${profile_src}>`
        modal_content += `<div class="follow-name">${f_datas[i].follower_name}</div>`
        modal_content += `</a>`
        modal_content += `</div>`
      }
      followersmodel.innerHTML = modal_content
  })
})