$(function(){

    $(document).on("click", "#add-product", function (e) {
        e.preventDefault();

        $next_id = parseInt($("#id_form-TOTAL_FORMS").attr('value'));
        $last_id = String($next_id - 1);

        $next_elem_prefix = "id_form-" + $next_id;
        $next_elem =
            "<tr id='" + $next_elem_prefix + "-tr'>" +
                "<td><input id='" + $next_elem_prefix + "-description' maxlength='255' name='" + $next_elem_prefix + "-description' type='text' /></td>" +
                "<td><input id='" + $next_elem_prefix + "-part_no' maxlength='255' name='" + $next_elem_prefix + "-part_no' type='text' /></td>" +
                "<td><input id='" + $next_elem_prefix + "-brand' maxlength='255' name='" + $next_elem_prefix + "-brand' type='text' /></td>" +
                "<td><input id='" + $next_elem_prefix + "-quantity' maxlength='255' name='" + $next_elem_prefix + "-quantity' type='text' /></td>" +
                "<td><input id='" + $next_elem_prefix + "-unit' maxlength='255' name='" + $next_elem_prefix + "-unit' type='text' /></td>" +
                "<td><a href='#'>remove</a></td>" +
            "</tr>";

        $("#id_form-" + $last_id + "-tr").after($next_elem);
        $("#id_form-TOTAL_FORMS").attr('value', $next_id + 1);
    });

});
