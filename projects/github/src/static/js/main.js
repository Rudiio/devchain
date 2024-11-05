// Axios CDN for making HTTP requests
document.write('<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"><\/script>');

function submitSearch(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Retrieve the input value from the search form
    const repositoryName = document.getElementById('repository-name').value;

    // Send a POST request to the '/search' endpoint with the repository name
    axios.post('/search', { repository_name: repositoryName })
        .then(function (response) {
            // Handle the response by updating the DOM with the received statistics
            updateStatistics(response.data);
        })
        .catch(function (error) {
            // Handle any errors here
            console.error('Error fetching repository data:', error);
            alert('Failed to fetch repository data. Please try again.');
        });
}

function updateStatistics(stats) {
    // Update the DOM elements with the received statistics
    document.getElementById('stars').textContent = stats.stars;
    document.getElementById('forks').textContent = stats.forks;
    document.getElementById('watchers').textContent = stats.watchers;
    document.getElementById('open-issues').textContent = stats.open_issues;
}

// Attach the 'submitSearch' function to the search form's 'submit' event
document.getElementById('search-form').addEventListener('submit', submitSearch);
