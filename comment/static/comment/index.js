$(document).ready(function () {
  $(".btn-nostyle").on("click", function () {
    $(".btn-nostyle").removeClass("active");
    $(this).toggleClass("active");
    const postId = $(this).data("post-id");
    const isUpvote = $(this).data("is-upvote");

    $.ajax({
      url: "/vote/",
      type: "POST",
      data: {
        post_id: postId,
        is_upvote: isUpvote,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        $(`#total-votes-${postId}`).text(response.total_votes);
      },
      error: function (response) {
        alert("An error occurred. Please try again.");
      },
    });
  });
  $(".message_count").on("click", function () {
    $(".comment_section").toggleClass("active");
    $(".comment-form").toggleClass("active");
  });
});
