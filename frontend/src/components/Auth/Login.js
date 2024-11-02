import React, { useState, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import API from '../../api';
import { useNavigate } from 'react-router-dom';

function Login() {
  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await API.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true, // Include this to send cookies
      });

      // Set the authenticated user in context
      setUser(formData.username);

      // Redirect to the dashboard
      navigate('/dashboard');
    } catch (err) {
      // More specific error handling
      setError(err.response?.data?.message || 'Invalid credentials');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          name="username"
          placeholder="Username"
          onChange={handleChange}
          value={formData.username}
          required
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          onChange={handleChange}
          value={formData.password}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;

