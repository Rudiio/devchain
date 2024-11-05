// /static/score.js

let score = 0; // Variable to keep track of the current score

// Function to update the score display in the DOM
export function updateScoreDisplay(newScore) {
    score = newScore; // Update the internal score variable
    const scoreElement = document.querySelector('#score-display'); // Select the score display element
    scoreElement.textContent = score; // Set the text content to the new score
}

// Additional function to add to the score
export function addToScore(points) {
    score += points; // Add the points to the current score
    updateScoreDisplay(score); // Update the score display
}

// Function to reset the score to zero
export function resetScore() {
    score = 0; // Reset the score variable
    updateScoreDisplay(score); // Update the score display
}
