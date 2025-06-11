// frontend/src/components/billing/ItemSearchModal.jsx
import React, { useEffect, useRef } from 'react';
import './ItemSearchModal.css';
import PropTypes from 'prop-types';

const ItemSearchModal = ({ searchResults, onSelect, onClose }) => {
  const modalRef = useRef(null);
  const [selectedIndex, setSelectedIndex] = React.useState(0);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => Math.min(prev + 1, searchResults.length - 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => Math.max(prev - 1, 0));
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (searchResults[selectedIndex]) {
          onSelect(searchResults[selectedIndex]);
        }
      } else if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [searchResults, selectedIndex, onSelect, onClose]);

  return (
    <div className="item-search-modal" ref={modalRef}>
      <div className="search-results">
        {searchResults.map((item, index) => (
          <div
            key={item.id}
            className={`search-result-item ${index === selectedIndex ? 'selected' : ''}`}
            onClick={() => onSelect(item)}
            onMouseEnter={() => setSelectedIndex(index)}
          >
            <div className="item-info">
              <span className="item-code">{item.item_code}</span>
              <span className="item-name">{item.name}</span>
              {item.size && <span className="item-size">{item.size}</span>}
            </div>
            <div className="item-details">
              <span className="item-stock">Stock: {item.current_stock}</span>
              <span className="item-price">₹{item.selling_price}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ItemSearchModal;

// At the bottom of the file
ItemSearchModal.propTypes = {
  searchResults: PropTypes.array.isRequired,
  onSelect: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired
};