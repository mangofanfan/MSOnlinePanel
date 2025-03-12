function validate() {
    var messages = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        messages[_i] = arguments[_i];
    }
    var errors = [];
    for (var _a = 0, messages_1 = messages; _a < messages_1.length; _a++) {
        var message = messages_1[_a];
        if (message[1] == "") {
            var msg = { name: message[0], value: "输入值为空" };
            errors.push(msg);
        }
        if (message[0] == "password") {
            if (message[1].length < 8) {
                var msg = { name: message[0], value: "密码长度过短，长度应大于等于8" };
                errors.push(msg);
            }
        }
        if (message[0] == "phone_number") {
            if (message[1].length != 11) {
                var msg = { name: message[0], value: "电话号码需要为11位数字" };
                errors.push(msg);
            }
        }
    }
    return errors;
}
function generateMsg(errors) {
    var message = "";
    for (var _i = 0, errors_1 = errors; _i < errors_1.length; _i++) {
        var error = errors_1[_i];
        message += "[ ".concat(error.name, " ] ").concat(error.value, "<br>");
    }
    return message;
}
