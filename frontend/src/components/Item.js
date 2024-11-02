import React, { useState, useEffect } from 'react';
import API from '../api';
import CollapsibleItem from './CollapsibleItem';

function Item({ item, refreshItems, level = 1 }) {
  const [subItems, setSubItems] = useState([]);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [newSubItemTitle, setNewSubItemTitle] = useState('');

  const fetchSubItems = async () => {
    const res = await API.get(`/items/${item.list_id}`);
    setSubItems(
      res.data.items.filter((subItem) => subItem.parent_item_id === item.item_id)
    );
  };

  useEffect(() => {
    if (level < 3) {
      fetchSubItems();
    }
  }, [item.item_id]);

  const handleAddSubItem = async () => {
    await API.post('/items/', {
      list_id: item.list_id,
      parent_item_id: item.item_id,
      title: newSubItemTitle,
    });
    setNewSubItemTitle('');
    fetchSubItems();
  };

  const handleToggleComplete = async () => {
    await API.put(`/items/${item.item_id}`, { is_completed: !item.is_completed });
    refreshItems();
  };

  const handleDelete = async () => {
    await API.delete(`/items/${item.item_id}`);
    refreshItems();
  };

  return (
    <li>
      <div style={{ marginLeft: level * 20 }}>
        <span
          style={{ textDecoration: item.is_completed ? 'line-through' : 'none' }}
        >
          {item.title}
        </span>
        <button onClick={handleToggleComplete}>
          {item.is_completed ? 'Undo' : 'Complete'}
        </button>
        <button onClick={handleDelete}>Delete</button>
        {level < 3 && (
          <>
            <button onClick={() => setIsCollapsed(!isCollapsed)}>
              {isCollapsed ? 'Expand' : 'Collapse'}
            </button>
            {!isCollapsed && (
              <>
                <input
                  value={newSubItemTitle}
                  onChange={(e) => setNewSubItemTitle(e.target.value)}
                  placeholder="New Sub-Item"
                />
                <button onClick={handleAddSubItem}>Add Sub-Item</button>
                <ul>
                  {subItems.map((subItem) => (
                    <Item
                      key={subItem.item_id}
                      item={subItem}
                      refreshItems={fetchSubItems}
                      level={level + 1}
                    />
                  ))}
                </ul>
              </>
            )}
          </>
        )}
      </div>
    </li>
  );
}

export default Item;
