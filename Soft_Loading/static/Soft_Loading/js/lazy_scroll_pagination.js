let page = 1;
$(document).ready(function () {
//            window.news_index = '{% url 'blog:posts' %}';


            let block_request = false;
            let end_pagination = false;

            $(window).scroll(function () {
                let margin = $(document).height() - $(window).height() - 10;

                if ($(window).scrollTop() > margin && end_pagination === false && block_request === false) {
//                    block_request = true;
                      page += 1;
                    window.location.search =  "?page=" + page;


//                    $.ajax({
//                        type: 'GET',
//
//                        data: {
//                            "page": page
//                        },
//                        success: function (data) {
//                            if (data.end_pagination === true) {
//                                end_pagination = true;
//                                page += 1;
//                            } else {
//                                block_request = false;
//                            }
//                            $('.board').append(data.content);
//                        }
//                    })
                }
            });
        })