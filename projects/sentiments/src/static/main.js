// main.js

document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyzeButton');
    const inputText = document.getElementById('inputText');
    const resultArea = document.getElementById('resultArea');

    analyzeButton.addEventListener('click', function() {
        const text = inputText.value.trim();
        if (text) {
            analyzeSentiment(text);
        } else {
            updateResultArea('Please enter some text to analyze.', 'neutral');
        }
    });

    function analyzeSentiment(text) {
        const apiUrl = '/analyze-sentiment'; // Updated API endpoint to match the backend route
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: { text: text } }), // Modified to match the expected request body format
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                updateResultArea(data.error, 'neutral');
            } else {
                updateResultArea(`Sentiment: ${data.sentiment}`, data.sentiment);
            }
        })
        .catch(error => {
            updateResultArea('An error occurred while analyzing the text.', 'neutral');
            console.error('Error:', error);
        });
    }

    function updateResultArea(message, sentiment) {
        resultArea.textContent = message;
        resultArea.className = ''; // Reset classes
        resultArea.classList.add('result-area', sentiment);
    }
});
