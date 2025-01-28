const testEmail = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;

export const LoginValidation = (email, password) => {
    if (email.trim() === '') {
        alert("Email required!", "bottom-right", "error");
        document.getElementById('email').focus();
        return false;
    } else if (!email.match(testEmail)) {
        alert("Invalid email address!", "bottom-right", "error");
        document.getElementById('email').focus();
        return false;
    } else if (password.trim() === '') {
        alert("Password is required!", "bottom-right", "error");
        document.getElementById('pasword').focus();
        return false;
    } else if (password.length < 6) {
        alert("Password must be at least 6 characters long!", "bottom-right", "error");
        document.getElementById('pasword').focus();
        return false;
    } else {
        return true;
    }
}

export const alert = (message, position, type = '') => {
    alertify.set("notifier", "position", position);
    switch (type) {
        case 'success':
            return alertify.success(message).dismissOthers();;
            break;
        case 'error':
            return alertify.error(message).dismissOthers();;
            break;
        case 'warning':
            return alertify.warning(message).dismissOthers();;
            break;
        default:
            return alertify.notify(message).dismissOthers();;
            break;
    }
}
