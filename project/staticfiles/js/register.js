// show password toggle
// 
const password = document.getElementById('id_password')
const showPassToggle = document.getElementById('showPassToggle')

showPassToggle.addEventListener('click', () => {
    if (showPassToggle.checked == true) {
        password.setAttribute('type', 'text')
    }else{
        password.setAttribute('type', 'password')
    }
    
})


// Username validation
// 
const username = document.getElementById('id_username')
const usernameHelp = document.getElementById('usernameHelp')
const usernameSpinner = document.getElementById('username-spinner')

usernameSpinner.style.display = 'none'

username.addEventListener('keyup', (e) => {

    const usernameVal = e.target.value;
    // start spinner
    usernameSpinner.style.display = 'block'

    usernameHelp.classList.remove('text-danger')
    username.classList.remove('is-invalid', 'is-valid')

    if (usernameVal.length > 0) {
        fetch('/auth/validate-username/', {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            usernameSpinner.style.display = 'none'
            if (data.username_error) {
                usernameHelp.classList.add('text-danger')
                username.classList.add('is-invalid')
            }else{
                username.classList.add('is-valid')
            }
        })
        .catch(err => console.log(err))
    }else{
        usernameSpinner.style.display = 'none'
    }
    
})


// Email validation
// 
const email = document.getElementById('id_email')
const emailHelp = document.getElementById('emailHelp')
const emailSpinner = document.getElementById('email-spinner')
emailSpinner.style.display = 'none'

email.addEventListener('keyup', (e) => {

    const emailVal = e.target.value;
    // start spinner
    emailSpinner.style.display = 'block'

    emailHelp.classList.remove('text-danger')
    email.classList.remove('is-invalid', 'is-valid')

    if (emailVal.length > 0) {
        fetch('/auth/validate-email/', {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            emailSpinner.style.display = 'none'
            if (data.email_error) {
                emailHelp.classList.add('text-danger')
                email.classList.add('is-invalid')
            }else{
                email.classList.add('is-valid')
            }
        })
        .catch(err => console.log(err))
    }else{
        emailSpinner.style.display = 'none'
    }
    
})


