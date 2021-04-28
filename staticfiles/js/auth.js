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