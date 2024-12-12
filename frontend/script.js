document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    fetchSolrResults(query);
});

function fetchSolrResults(query) {
    const url = `http://localhost:8983/solr/true_crime/select?q=${encodeURIComponent(query)}&wt=json`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const results = data.response.docs;
            displayResults(results);
        })
        .catch(error => console.error('Error fetching Solr results:', error));
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    if (results.length === 0) {
        resultsDiv.innerHTML = '<p>No results found.</p>';
        return;
    }

    const list = document.createElement('ul');
    results.forEach(result => {
        const listItem = document.createElement('li');
        listItem.textContent = JSON.stringify(result); // Customize display as needed
        list.appendChild(listItem);
    });
    resultsDiv.appendChild(list);
}
