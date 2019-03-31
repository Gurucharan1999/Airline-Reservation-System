$(function() {
    $("#id_source").keyup(function() {
        $.ajax({
            type: "POST",
            url: "/index/srchsrc/",
            data: {
                "src_txt" : $("#id_source").val(),
                "csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(data) {
                $("#srcres").html(data);
            },
            dataType: "html"
        });
    });
});

$(function() {
    $("#id_destination").keyup(function() {
        $.ajax({
            type: "POST",
            url: "/index/srchdst/",
            data: {
                "dst_txt" : $("#id_destination").val(),
                "csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(data) {
                $("#dstres").html(data);
            },
            dataType: "html"
        });
    });
});