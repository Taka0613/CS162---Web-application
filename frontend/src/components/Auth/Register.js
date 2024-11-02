import React, { useState } from 'react';
import API from '../../api';
import { useNavigate } from 'react-router-dom';

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form Data being sent:', formData);  // Debugging line

    try {
      // Make the API request to register the user
      const response = await API.post('/auth/register', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Registration successful, response:', response.data);  // Debugging line

      // Redirect to the homepage on successful registration
      navigate('/');
    } catch (err) {
      console.error('Full error object:', err);  // Log the full error object for insight
      console.error('Registration error details:', err.response ? err.response.data : err.message);  // More detailed error logging
      
      // Set an appropriate error message based on the error response
      if (err.response) {
        // If there is a response from the server, display the specific error message
        setError(err.response.data.message || 'An error occurred during registration');
      } else if (err.request) {
        // If there was no response from the server (e.g., network error)
        setError('No response from the server. Please check your network.');
      } else {
        // Any other errors
        setError('An error occurred during registration');
      }
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
