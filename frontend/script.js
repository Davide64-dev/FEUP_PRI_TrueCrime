document.getElementById('searchForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const userInput = document.getElementById('query').value.trim();
    if (userInput) {
        if (isAdvancedQuery(userInput)) {
            // Handle advanced query directly
            console.log('Handling advanced query:', userInput);
            fetchSolrResults(userInput, true);
        } else {
            // Build dynamic query from simple input
            console.log('Building dynamic query for:', userInput);
            fetchSolrResults(buildDynamicQuery(userInput), false);
        }
    } else {
        displayResults([]);
    }
});

document.querySelectorAll('.sort-button').forEach(button => {
    button.addEventListener('click', function () {
        const sortField = this.getAttribute('data-sort');
        sortResults(sortField);
    });
});



function isAdvancedQuery(input) {
    // Check for common Solr query syntax like :, AND, OR, ~, etc.
    const advancedQueryKeywords = /[\(\):"~^]/;
    return advancedQueryKeywords.test(input);
}

function buildDynamicQuery(userInput) {
    return `(Title:(${userInput}~1)^2 OR transcript:(${userInput}~1)) AND (Title:"${userInput}"~5^3 OR transcript:"${userInput}"~5)`;
}

function fetchSolrResults(query, isRawQuery) {
    const url = `http://localhost:8983/solr/true_crime/select?${isRawQuery ? 'q' : 'q'}=${encodeURIComponent(query)}&wt=json`;

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
    resultsDiv.innerHTML = '';

    if (results.length === 0) {
        resultsDiv.innerHTML = '<p>No results found.</p>';
        return;
    }

    const list = document.createElement('ul');
    results.forEach(result => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <div class="video-item">
                <img src="https://img.youtube.com/vi/${result.videoId}/0.jpg" alt="${result.Title || 'Video'} Thumbnail" class="video-thumbnail">
                <div class="video-info">
                    <p><strong>Title:</strong> ${result.Title || 'N/A'}</p>
                    <p><strong>Views:</strong> ${result.Views || 'N/A'}</p>
                    <p><strong>Likes:</strong> ${result.Likes || 'N/A'}</p>
                    <p><strong>Link:</strong> <a href="https://www.youtube.com/watch?v=${result.videoId}" target="_blank">https://www.youtube.com/watch?v=${result.videoId}</a></p>
                </div>
            </div>
        `;
        list.appendChild(listItem);
    });
    resultsDiv.appendChild(list);
}

function sortResults(field) {
    const resultsDiv = document.getElementById('results');
    const listItems = Array.from(resultsDiv.querySelectorAll('li'));

    listItems.sort((a, b) => {
        const aValue = parseFieldValue(a, field);
        const bValue = parseFieldValue(b, field);
        return bValue - aValue; // Sort in descending order
    });

    const sortedList = document.createElement('ul');
    listItems.forEach(item => sortedList.appendChild(item));

    resultsDiv.innerHTML = '';
    resultsDiv.appendChild(sortedList);
}

// Helper function to extract numeric values for the given field
function parseFieldValue(listItem, field) {
    const paragraphs = Array.from(listItem.querySelectorAll('p'));
    const fieldParagraph = paragraphs.find(p => p.textContent.includes(field + ':'));
    if (fieldParagraph) {
        const fieldValue = parseInt(fieldParagraph.textContent.split(': ')[1]) || 0;
        return fieldValue;
    }
    return 0;
}