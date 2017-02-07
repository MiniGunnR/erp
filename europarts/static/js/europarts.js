$(function() {
    $(document).on("focusout", "[id^=id_form-][id$=-part_no]", function() {

        $this = $(this);

        url = "/europarts/get/part/" + $(this).val() + "/info/";

        $.getJSON(url, function(data) {
            var description = data['description'];
            var brand = data['brand'];

            $this.parent().next().find('input').val(description);
            $this.parent().next().next().find('input').val(brand);
            $this.parent().next().next().next().find('input').focus();
        });
    })
});
