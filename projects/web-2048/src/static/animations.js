// /static/animations.js

export function animateTileMovement(tileId, newPosition) {
    const tile = document.getElementById(tileId);
    if (tile) {
        // Assuming newPosition is an object with x and y properties
        const newLeft = newPosition.x * (tile.offsetWidth + 10); // 10 is the grid-gap from CSS
        const newTop = newPosition.y * (tile.offsetHeight + 10);

        tile.style.transition = 'left 0.2s, top 0.2s'; // Smooth transition for movement
        tile.style.left = `${newLeft}px`;
        tile.style.top = `${newTop}px`;
    }
}

export function animateTileMerge(tileId, newPosition, newTileValue) {
    const tile = document.getElementById(tileId);
    if (tile) {
        // Move the tile to the merge position
        animateTileMovement(tileId, newPosition);

        // Set a timeout to wait for the movement to finish before starting the merge animation
        setTimeout(() => {
            tile.textContent = newTileValue; // Update the tile's number
            tile.style.transition = 'transform 0.1s'; // Smooth transition for scaling
            tile.style.transform = 'scale(1.1)'; // Scale up the tile

            // Set another timeout to shrink the tile back to its original size
            setTimeout(() => {
                tile.style.transform = 'scale(1)'; // Reset the scale
            }, 100); // Wait 100ms before shrinking back
        }, 200); // Wait 200ms for the movement to finish
    }
}
