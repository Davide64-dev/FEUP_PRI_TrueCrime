import React, { useState } from 'react';
import { fetchResults } from '../solrApi';

const SearchBar = ({ onResults }) => {
    const [query, setQuery] = useState('');

    const handleSearch = async () => {
        try {
            const results = await fetchResults(query);
            onResults(results);
        } catch (error) {
            console.error("Error during search:", error);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search..."
            />
            <button onClick={handleSearch}>Search</button>
        </div>
    );
};

export default SearchBar;
