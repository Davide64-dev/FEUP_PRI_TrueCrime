import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import Results from './components/Results';   
const App = () => {
    const [results, setResults] = useState([]);
    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1 style={{ textAlign: 'center', color: '#333' }}>True Crime Search</h1>
            <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                <SearchBar setResults={setResults} />
                
                <Results results={results} />
            </div>
        </div>
    );
};
export default App;