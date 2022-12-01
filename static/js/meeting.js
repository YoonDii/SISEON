/* 카테고리 버튼 */
$(function () {
  $("#test1").on("click", function () {
      console.log(1)
      $("#first").show();
  });
  $("#test1").on("click", function () {
      $("#second").hide();
  });
});


$(function () {
  $("#test2").on("click", function () {
      $("#second").show();
  });
  $("#test2").on("click", function () {
      $("#first").hide();
  });
});


$(document).ready(function () {
  $("#test1").trigger("click");
});

var focused = null;
$(".test1").focus(function () {
  focused = $(this);
});

