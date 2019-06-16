$(".accept_ecopoint").click(function () {
    var url = $("#ecopointsForAprove").attr("data-ecopoints-url");
    var id_to_update = $(this).parent().attr("data-ecopoint-id");
    $.ajax({
        url: url,
        data: {
            'point_request_id': id_to_update,
            'change_type': 'approved'
        },
        success: function (data) {
            $('#bodytable').html(data);
        }
    });

});
$(".decline_ecopoint").click(function () {
    var url = $("#ecopointsForAprove").attr("data-ecopoints-url")
    var id_to_update = $(this).parent().attr("data-ecopoint-id");
    $.ajax({
        url: url,
        data: {
            'point_request_id': id_to_update,
            'change_type': 'declined'
        },
        success: function (data) {
            $('#bodytable').html(data);
        }
    });

});