const wrapper = document.querySelector('.wrapper');
const registerLink = document.querySelector('.register-link');
const loginLink = document.querySelector('.login-link');
const loginForm = document.querySelector('.form-box.login form');
const registerForm = document.querySelector('.form-box.register form');

const API_BASE_URL = 'http://127.0.0.1:8000/api/users';

registerLink.onclick = () => {
  wrapper.classList.add('active');
};

loginLink.onclick = () => {
  wrapper.classList.remove('active');
};

// Login API Call
loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const emailInput = loginForm.querySelector('input[type="text"]');
  const passwordInput = loginForm.querySelector('input[type="password"]');

  const email = emailInput.value.trim();
  const password = passwordInput.value;

  if (!email || !password) {
    alert('Please fill in both email and password.');
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
      alert('Login successful!');
      localStorage.setItem('access_token', data.access || data.token);
      if (data.refresh) {
        localStorage.setItem('refresh_token', data.refresh);
      }
      window.location.href = 'dashboard.html';
    } else if (data.error && data.error.includes('email does not exist')) {
      alert('Email does not exist. Please sign up.');
      wrapper.classList.add('active'); // Switch to sign-up form
    } else if (data.error && data.error.includes('incorrect password')) {
      alert('Incorrect password. Please try again.');
    } else {
      alert(data.detail || data.error || 'Login failed. Please try again.');
    }
  } catch (error) {
    console.error('Error during login:', error);
    alert('An error occurred during login. Please try again later.');
  }
});

// Registration API Call with Confirm Password & Email Existence Check
registerForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const usernameInput = registerForm.querySelector('input[type="text"]');
  const emailInput = registerForm.querySelector('input[type="email"]');
  const passwordInput = registerForm.querySelectorAll('input[type="password"]')[0];
  const confirmPasswordInput = registerForm.querySelectorAll('input[type="password"]')[1];

  const username = usernameInput.value.trim();
  const email = emailInput.value.trim();
  const password = passwordInput.value;
  const confirmPassword = confirmPasswordInput.value;

  if (!username || !email || !password || !confirmPassword) {
    alert('Please fill in all fields.');
    return;
  }

  if (password !== confirmPassword) {
    alert('Passwords do not match.');
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, email, password , confirm_password: confirmPassword })
    });

    const data = await response.json();

    if (response.ok) {
      alert('Registration successful! Please log in.');
      wrapper.classList.remove('active'); // Switch to login form
    } else if (data.error && data.error.includes('email already exists')) {
      alert('Email already exists. Please go to login.');
      wrapper.classList.remove('active'); // Switch to login form
    } else {
      alert(data.error || data.detail || 'Registration failed. Please try again.');
    }
  } catch (error) {
    console.error('Error during registration:', error);
    alert('An error occurred during registration. Please try again later.');
  }
});
