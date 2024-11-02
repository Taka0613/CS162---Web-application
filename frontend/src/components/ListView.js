import React, { useState, useEffect } from 'react';
import API from '../api';
import { useParams } from 'react-router-dom';
import Item from './Item';

function ListView() {
  const { listId } = useParams();
  const [listTitle, setListTitle] = useState('');
  const [items, setItems] = useState([]);
  const [newItemTitle, setNewItemTitle] = useState('');

  const fetchList = async () => {
    const res = await API.get(`/lists/${listId}`);
    setListTitle(res.data.title);
  };

  const fetchItems = async () => {
    const res = await API.get(`/items/${listId}`);
    setItems(res.data.items.filter((item) => item.parent_item_id === null));
  };

  useEffect(() => {
    fetchList();
    fetchItems();
  }, [listId]);

  const handleAddItem = async () => {
    await API.post('/items/', { list_id: listId, title: newItemTitle });
    setNewItemTitle('');
    fetchItems();
  };

  return (
    <div>
      <h2>{listTitle}</h2>
      <input
        value={newItemTitle}
        onChange={(e) => setNewItemTitle(e.target.value)}
        placeholder="New Item"
      />
      <button onClick={handleAddItem}>Add Item</button>
      <ul>
        {items.map((item) => (
          <Item key={item.item_id} item={item} refreshItems={fetchItems} />
        ))}
      </ul>
    </div>
  );
}

export default ListView;
