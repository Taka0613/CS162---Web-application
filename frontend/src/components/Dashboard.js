import React, { useState, useEffect } from 'react';
import API from '../api';
import { Link } from 'react-router-dom';

function Dashboard() {
  const [lists, setLists] = useState([]);
  const [newListTitle, setNewListTitle] = useState('');
  const [error, setError] = useState('');

  const fetchLists = async () => {
    try {
      const res = await API.get('/lists/', { withCredentials: true });
      setLists(res.data.lists);
      setError('');  // Clear any previous error on success
    } catch (err) {
      console.error("Error fetching lists:", err);
      setError("Unable to fetch lists. Please ensure you are logged in.");
    }
  };

  useEffect(() => {
    fetchLists();
  }, []);

  const handleCreateList = async () => {
    if (!newListTitle.trim()) {
      setError("List title cannot be empty.");
      return;
    }

    try {
      await API.post(
        '/lists/',
        { title: newListTitle },
        { withCredentials: true }
      );
      setNewListTitle('');
      setError('');  // Clear any previous error on success
      fetchLists();
    } catch (err) {
      console.error("Error creating list:", err);
      setError("Failed to create list. Please try again.");
    }
  };

  return (
    <div>
      <h2>Your Lists</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <input
        value={newListTitle}
        onChange={(e) => setNewListTitle(e.target.value)}
        placeholder="New List Title"
      />
      <button onClick={handleCreateList}>Create List</button>
      <ul>
        {lists.map((lst) => (
          <li key={lst.list_id}>
            <Link to={`/lists/${lst.list_id}`}>{lst.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
