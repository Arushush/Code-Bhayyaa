document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the form from submitting the default way

    // Get email and password from the form
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    console.log(email)
    console.log(password)

    try {
        const response = await fetch('http://127.0.0.1:5000/login', {  // Ensure this matches your Flask route '/login'
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'email': email,
                'password': password,
            })
        });

        const result = await response.json();
        if (response.ok && result.status !== false) {
            // Handle success (e.g., navigate to another page or show success message)
            alert(result.message);
            console.log(result.uid); // User's UID
        } else if (result.status == false ) {
            // Handle error (e.g., show error message)
            alert(result.error);
        }
    } catch (error) {
        console.error('Error logging in:', error);
    }
});
