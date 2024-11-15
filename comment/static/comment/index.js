$(document).ready(function () {
  $(".btn-nostyle").on("click", function () {
    $(".btn-nostyle").removeClass("active");
    $(this).toggleClass("active");
  });
});
