$(document).ready(function () {
  $(".like-button").click(function (event) {
    // Get required data
    let target = $(event.currentTarget);
    let croak_id = target.data("id");
    let croak_action = target.data("action");
    let croak_like_url = target.data("like-url");

    // Get icon and count elements
    let like_icon = target.find(".like-icon");
    let like_count = target.find(".like-count");

    // Make ajax request to croak url sending croak id and action
    $.ajax({
      url: croak_like_url,
      data: {
        croak_id: croak_id,
        croak_action: croak_action,
      },
    }).done(function (data) {
      // When complete, check to see if was successful
      if (data.success) {
        // console.log(data);
        let action = data.action;
        let total_like_count = data.like_count;
        console.log(action);
        console.log(total_like_count);
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
