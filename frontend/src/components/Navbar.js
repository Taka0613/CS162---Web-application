import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import API from '../api';
import { useNavigate, Link } from 'react-router-dom';

function Navbar() {
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    await API.post('/auth/logout');
    setUser(null);
    navigate('/');
  };

  return (
    <nav>
      <h1>Hierarchical Todo List App</h1>
      {user ? (
        <>
          <span>Welcome, {user}</span>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/">Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </nav>
  );
}

export default Navbar;
