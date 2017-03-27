$(function() {

    $(document).on("change", "[id^=id_form][id$=brand]", function() {
        var $value = $(this).val();

        var $id_prefix = $(this).attr('id').slice(0, -5);
        $auto_type = $("#" + $id_prefix + "auto_type");

        $.ajax({
            type: 'GET',
            url: '/europarts_old_2/filter/auto/type/with/brand/' + String($value),

            success: function(data) {
                $auto_type.html(data);
            }
        });
    });

    $(document).on("focusout", "[id^=id_form-][id$=-part_no]", function() {

        $part_no = $(this).val();

        var $id_prefix = $(this).attr('id').slice(0, -7);
        $brand_id = $("#" + $id_prefix + "brand").val();

        $.ajax({
            type: 'GET',
            url: '/europarts_old_2/fetch/from/part/no/' + $part_no + '/brand/' + $brand_id,

            success: function(data) {
                $("#" + $id_prefix + "description").val(data['description']);
                $("#" + $id_prefix + "quantity").val(1).focus();
            }
        });
    });

    $(".quotation-add-btn").on("click", function(e) {
        e.preventDefault();

        $qty_input = $(this).parent().prev();
        console.log($qty_input.val());
        console.log($qty_input.attr('data-product'));
    });

    $("#auto_parts").on("change", function() {
        var $value = $(this).val();

        $.ajax({
            type: 'GET',
            url: '/europarts_old_2/fetch/product/from/auto/part/' + String($value),

            success: function(data) {
                $("#description").html(data['description']);
                $("#price").html(data['price']);
            }
        });
    });

    $("#add-product-to-quotation").on("click", function(e) {
        e.preventDefault();

        var $product = $("#auto_parts").val();
    });

    $("#print-work-order-btn").on("click", function(e) {
        e.preventDefault();

        $pk = $(this).attr('data-id');

        $url = "/europarts_old_2/disable/work/order/print/" + $pk + "/";

        $.get(url=$url);
    });

});
