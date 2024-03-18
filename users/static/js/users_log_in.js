//настроить

const registrationForm = document.getElementById('registrationForm')

registrationForm.addEventListener('submit', function (event) {
	event.preventDefault() // Предотвращаем отправку формы

	const username = document.getElementById('username').value
	const email = document.getElementById('email').value
	const password = document.getElementById('password').value

	console.log('Username:', username)
	console.log('Email:', email)
	console.log('Password:', password)

	// дальнейшая обработка
})
