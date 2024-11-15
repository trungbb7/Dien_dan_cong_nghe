$(document).ready(function () {
  $(".btn-nostyle").on("click", function () {
    $(".btn-nostyle").removeClass("active");
    $(this).toggleClass("active");
  });
  $(".message_count").on("click", function () {
    $(".comment_section").toggleClass("active");
    $(".comment-form").toggleClass("active");

  });
});
