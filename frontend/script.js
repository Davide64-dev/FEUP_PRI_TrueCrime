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
    const url = `http://localhost:8983/solr/true_crime/select?${isRawQuery ? 'q' : 'q'}=${encodeURIComponent(query)}&hl=true&hl.fl=Description,transcript&hl.simple.pre=<mark>&hl.simple.post=</mark>&wt=json`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const results = data.response.docs;
            const highlights = data.highlighting; // Get the highlighting section
            displayResults(results, highlights);
        })
        .catch(error => console.error('Error fetching Solr results:', error));
}

function displayResults(results, highlights) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (results.length === 0) {
        resultsDiv.innerHTML = '<p>No results found.</p>';
        return;
    }

    const list = document.createElement('ul');

    results.forEach(result => {

        const highlight = highlights[result.id] || {};
        let descriptionSnippet = highlight.Description ? extractContext(highlight.Description[0]) : 'No relevant description found.';
        let transcriptSnippet = highlight.transcript ? extractContext(highlight.transcript[0]) : 'No relevant transcript snippet found.';

        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <div class="video-item">
                <iframe class="video-video"
                    width="300" 
                    height="200" 
                    src="https://www.youtube.com/embed/${result.videoId}" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                </iframe>
                <div class="video-info">
                    <h3><strong>${result.Title || 'N/A'}</strong></h3>
                    <p><strong>Description Snippet:</strong> ${descriptionSnippet}</p>
                    <p><strong>Transcript Snippet:</strong> ${transcriptSnippet}</p>
                    <p><img src="imgs/icon-views.png" class="icon"> ${result.Views || 'N/A'}</p>
                    <p><img src="imgs/icon-like.png" class="icon"> ${result.Likes || 'N/A'}</p>
                </div>
            </div>
        `;
        list.appendChild(listItem);
    });

    resultsDiv.appendChild(list);
}

function extractContext(snippet, preTag = "<mark>", postTag = "</mark>", contextSize = 5) {
    const regex = new RegExp(`${preTag}(.*?)${postTag}`, "g");
    let match = regex.exec(snippet);

    if (match) {
        const highlightedText = match[1]; // The highlighted word/phrase
        const words = snippet.replace(/<[^>]+>/g, "").split(/\s+/); // Strip HTML tags and split into words
        const matchIndex = words.indexOf(highlightedText);

        if (matchIndex !== -1) {
            const start = Math.max(0, matchIndex - contextSize);
            const end = Math.min(words.length, matchIndex + contextSize + 1);
            const before = start > 0 ? "(...)" : ""; // Add "(...)" if there are words before the snippet
            const after = end < words.length ? "(...)" : ""; // Add "(...)" if there are words after the snippet
            const snippetWords = words.slice(start, end).join(" ");
            return `${before} ${snippetWords.replace(highlightedText, `${preTag}${highlightedText}${postTag}`)} ${after}`;
        }
    }

    // Return the original snippet with "(...)" on both ends if no match
    return `(...) ${snippet} (...)`;
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