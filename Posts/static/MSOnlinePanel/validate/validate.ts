interface ErrorMessage {
    name: string;
    value: string;
}

function validate(...messages: [string, string][]): ErrorMessage[] {
    let errors: ErrorMessage[] = [];
    for (let message of messages) {
        if (message[1] == "") {
            let msg: ErrorMessage = {name: message[0], value: "输入值为空"}
            errors.push(msg)
        }
        if (message[0] == "password") {
            if (message[1].length < 8) {
                let msg: ErrorMessage = {name: message[0], value: "密码长度过短，长度应大于等于8"}
                errors.push(msg)
            }
        }
        if (message[0] == "phone_number") {
            if (message[1].length != 11) {
                let msg: ErrorMessage = {name: message[0], value: "电话号码需要为11位数字"}
                errors.push(msg)
            }
        }
    }
    return errors;
}

function generateMsg(errors: ErrorMessage[]): string {
    let message = "";
    for (let error of errors) {
        message += `[ ${error.name} ] ${error.value}<br>`;
    }
    return message;
}
