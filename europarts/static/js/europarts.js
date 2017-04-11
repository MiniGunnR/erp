$(function() {

    $("input[id^='id_form-'][id$='-part_no']").on('blur', function(e) {
        var $part_no = $(this).val();
        var $url = '/europarts/fetch/item/details/' + $part_no + '/';
        var $id = $(this).attr('id').replace("id_form-", "").replace("-part_no", "");

        if ($part_no != "") {
            $.ajax({
                type: 'GET',
                url: $url,

                success: function(data){
                    console.log($id);
                    $("#id_form-" + $id + "-brand").val(data.brand);
                    $("#id_form-" + $id + "-type").val(data.type);
                    $("#id_form-" + $id + "-description").val(data.description);
                    $("#id_form-" + $id + "-cost_price").val(data.cost_price);
                    $("#id_form-" + $id + "-quantity").val(1).focus();
                }
            });
        }
    });

    $(".column-toggle").on('click', function(e) {
        e.preventDefault();

        var $url = $(this).attr('href');
        var $this = $(this);

        $.ajax({
            type: 'POST',
            url: $url,

            success: function(data) {
                $this.children('span').toggleClass("glyphicon-eye-open").toggleClass("glyphicon-eye-close");
            }
        });
    });

    $("input[id^='id_form-'][id$='-sale_price']")
        .on('focus', function(e) {
            var $this = $(this);

            $("#past_price")
                .show()
                .css({
                    'position': 'absolute',
                    'z-index': 100,
                    'top': $this.position().top + 26,
                    'left': $this.position().left,
                    'width': ($this.width() + 6),
                    //'height': ($this.height() + 6) * 7

                });

            var $id = $(this).attr('id').replace("id_form-", "").replace("-sale_price", "");
            $part_no = $("#id_form-" + $id + "-part_no").val();

            $.ajax({
                type: 'GET',
                url: '/europarts/get/past/price/' + $part_no + '/',

                success: function(data) {
                    html = '';
                    if (data != '') {
                        $.each(data, function(index, value) {
                            html += '<p>' + value + '</p>';
                        });
                    } else {
                        html = 'No data available.'
                    }
                    $("#past_price").html(html)
                }
            });
        })
        .on('blur', function(e) {
            $("#past_price").hide();

            var $id = $(this).attr('id').replace("id_form-", "").replace("-sale_price", "");

            var $cost_price = $("#id_form-" + $id + "-cost_price").val();

            if ($(this).val() != '') {
                $profit_margin = (($(this).val() - $cost_price) / $cost_price) * 100;

                $("#id_form-" + $id + "-profit_margin").val($profit_margin);
            }
        });

    $("input[id^='id_form-'][id$='-profit_margin']").on('blur', function(e) {
        var $id = $(this).attr('id').replace("id_form-", "").replace("-profit_margin", "");

        if ($(this).val() != '') {
            var $cost_price = $("#id_form-" + $id + "-cost_price").val();

            var $sale_price = $cost_price * (1 + ($(this).val() / 100));

            $("#id_form-" + $id + "-sale_price").val(Math.round($sale_price));
        }

    });

    //$("input[id^='id_form-'][id$='-sale_price']").on('blur', function(e) {
    //    $("#past_price").hide();
    //});

    $("input[id^='id_form-'][id$='-total']").on('focus', function(e) {
        var $id = $(this).attr('id').replace("id_form-", "").replace("-total", "");
        var $quantity = $("#id_form-" + $id + "-quantity").val();
        var $sale_price = $("#id_form-" + $id + "-sale_price").val();

        if ($quantity && $sale_price) {
            $total = $quantity * $sale_price;
            $("#id_form-" + $id + "-total").val($total);
        }
    });


    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // -! using jQuery

});

