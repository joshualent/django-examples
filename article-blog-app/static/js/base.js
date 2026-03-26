$(document).ready(function () {
  $(".like-button").click(function (event) {
    // Get required data
    let target = $(event.currentTarget);
    let article_id = target.data("id");
    let article_action = target.data("action");
    let article_like_url = target.data("like-url");

    // Get icon and count elements
    let like_icon = target.find(".like-icon");
    let like_count = target.find(".like-count");

    // console.log(target);
    // console.log(article_id);
    // console.log(article_action);
    // console.log(article_like_url);
    // Make ajax request to article url sending article id and action
    $.ajax({
      url: article_like_url,
      data: {
        article_id: article_id,
        article_action: article_action,
      },
    }).done(function (data) {
      // When complete, hceck to see if was cuessfull
      if (data.success) {
        // console.log(data);
        let action = data.action;
        let total_like_count = data.like_count;
        // If we liked, update elements to match.
        if (action === "like") {
          target.removeClass("btn-outline-primary");
          target.addClass("btn-primary");
          like_icon.removeClass("bi-hand-thumbs-up");
          like_icon.addClass("bi-hand-thumbs-up-fill");
          like_count.html(total_like_count);
          target.data("action", "unlike");
        } else {
          target.removeClass("btn-primary");
          target.addClass("btn-outline-primary");
          like_icon.removeClass("bi-hand-thumbs-up-fill");
          like_icon.addClass("bi-hand-thumbs-up");
          like_count.html(total_like_count);
          target.data("action", "like");
        }
      }
    });
  });
});
