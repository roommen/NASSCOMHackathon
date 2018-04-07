/* Show User Info */
function showUserInfo(){
    //get userid from browser local storage
    var user_id = localStorage.getItem("user_id");
    //API Endpoint - Replace this with endpoint you created
    var info_url = ' https://123abcdef789.execute-api.ap-south-1.amazonaws.com/lambda101/users';

    $.ajax({
        url: info_url,
        type: 'GET',
        data : {"user_id" : user_id},
        dataType: 'html',
        async: false,
        success: function(data)
        {
            var result = $.parseJSON(data);
            user_info = result['values'];
            html_code = "";

            html_code += '<td>' + user_info['name'] +
                    '</td><td>' + user_info['email'] + '</td><td>' + user_info['location'] + '</td><td>' + user_info['comments']
                    '</td><td><span style="color:#4ef71b;text-align:center;" class="fa fa-circle"></span>' +
                    '</td><td><div class="tooltip"><span class="tooltiptext">Block</span><a href="" class="block-user" style="color:red;"><span class="fa fa-ban"></span></a></div></td></tr>';

            $('#users-list tbody').html(html_code);
        }
    });
}

/* Get Aadhaar Info */
function getInfo(aadhaar_details)
{
	var result = null;
    if(aadhaar_details.aadhaar)
    {
        $("#otp").css('visibility', 'visible');
        $("#otp-label").css('visibility', 'visible');

        //API Endpoint - Replace this with endpoint you created
        aadhaar_url = 'https://123abcdef789.execute-api.ap-south-1.amazonaws.com/lambda101/login';
        var obj = new Object();
        obj.email = auth_details.email;
        obj.password = passwordValue;

        var jsonObj = JSON.stringify(obj);

        $.ajax({
            url: login_url,
            type: 'POST',
            data: jsonObj,
            dataType: 'json',
            success: function(result)
            {
                login_success = result['result'];
                //store userid in browser local storage
                if (typeof(Storage) !== "undefined") {
                    localStorage.setItem("aadhaar_id", result['aid']);
                }

                if(login_success === "true"){
                    aid = result['aid']
                    window.location = './info.html';
                }else{
                    $("#error").text("*Invalid OTP");
                    $("#error").css('visibility', 'visible');
                }
            },
        });
    }
}
