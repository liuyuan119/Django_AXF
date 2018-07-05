function password_hash() {

    var $password = $("#exampleInputPassword")

    var password = $password.val();

    $password.val(ma5(password));

    return true;


}