// /static/game.js

import { animateTileMovement, animateTileMerge } from './animations.js';
import { updateScoreDisplay, addToScore, resetScore } from './score.js';

const GRID_SIZE = 4;
const WIN_VALUE = 2048;

let gameState = {
  grid: [],
  score: 0,
  won: false,
  over: false
};

function initializeGameState() {
  gameState.grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(null));
  gameState.score = 0;
  gameState.won = false;
  gameState.over = false;
  resetScore();
  updateUI();
}

function startNewGame() {
  initializeGameState();
  addRandomTile();
  addRandomTile();
  updateUI();
}

function addRandomTile() {
  let emptyTiles = [];
  for (let row = 0; row < GRID_SIZE; row++) {
    for (let col = 0; col < GRID_SIZE; col++) {
      if (gameState.grid[row][col] === null) {
        emptyTiles.push({ x: col, y: row });
      }
    }
  }
  if (emptyTiles.length > 0) {
    const randomTile = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
    gameState.grid[randomTile.y][randomTile.x] = Math.random() < 0.9 ? 2 : 4;
    updateUI();
  }
}

function handleTileMovement(direction) {
  if (gameState.over || gameState.won) return;

  let hasMoved = false;
  let rotatedGrid = rotateGrid(gameState.grid, direction);
  for (let row = 0; row < GRID_SIZE; row++) {
    let currentRow = rotatedGrid[row].filter(tile => tile !== null);
    let newRow = [];

    while (currentRow.length > 0) {
      if (currentRow.length >= 2 && currentRow[0] === currentRow[1]) {
        const mergedValue = currentRow[0] * 2;
        newRow.push(mergedValue);
        addToScore(mergedValue);
        for (let col = 0; col < newRow.length; col++) {
          animateTileMerge(`tile-${row * GRID_SIZE + col + 1}`, {x: col, y: row}, mergedValue);
        }
        currentRow.splice(0, 2);
        hasMoved = true;
      } else {
        newRow.push(currentRow.shift());
      }
    }

    while (newRow.length < GRID_SIZE) {
      newRow.push(null);
    }

    for (let col = 0; col < GRID_SIZE; col++) {
      if (rotatedGrid[row][col] !== newRow[col]) {
        animateTileMovement(`tile-${row * GRID_SIZE + col + 1}`, {x: col, y: row});
        hasMoved = true;
      }
      rotatedGrid[row][col] = newRow[col];
    }
  }

  gameState.grid = rotateGrid(rotatedGrid, (4 - direction) % 4);

  if (hasMoved) {
    addRandomTile();
    updateUI();
    checkWinCondition();
    checkGameOver();
  }
}

function rotateGrid(grid, times) {
  let newGrid = grid;
  while (times > 0) {
    newGrid = newGrid[0].map((val, index) => newGrid.map(row => row[index]).reverse());
    times--;
  }
  return newGrid;
}

function updateUI() {
  for (let row = 0; row < GRID_SIZE; row++) {
    for (let col = 0; col < GRID_SIZE; col++) {
      let tileValue = gameState.grid[row][col];
      let tile = document.getElementById(`tile-${row * GRID_SIZE + col + 1}`);
      tile.textContent = tileValue || '';
      tile.className = `tile ${tileValue ? `tile-${tileValue}` : ''}`;
    }
  }
  updateScoreDisplay(gameState.score);
  if (gameState.won) {
    const gameMessage = document.getElementById('game-message');
    gameMessage.textContent = 'You won!';
  } else if (gameState.over) {
    const gameMessage = document.getElementById('game-message');
    gameMessage.textContent = 'Game Over!';
  }
}

function checkWinCondition() {
  for (let row = 0; row < GRID_SIZE; row++) {
    for (let col = 0; col < GRID_SIZE; col++) {
      if (gameState.grid[row][col] === WIN_VALUE) {
        gameState.won = true;
        updateUI();
        return;
      }
    }
  }
}

function checkGameOver() {
  let movesAvailable = false;
  for (let row = 0; row < GRID_SIZE; row++) {
    for (let col = 0; col < GRID_SIZE; col++) {
      if (gameState.grid[row][col] === null) {
        movesAvailable = true;
        break;
      }
      if (col !== GRID_SIZE - 1 && gameState.grid[row][col] === gameState.grid[row][col + 1]) {
        movesAvailable = true;
        break;
      }
      if (row !== GRID_SIZE - 1 && gameState.grid[row][col] === gameState.grid[row + 1][col]) {
        movesAvailable = true;
        break;
      }
    }
    if (movesAvailable) break;
  }
  if (!movesAvailable) {
    gameState.over = true;
    updateUI();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  startNewGame();
  document.getElementById('new-game').addEventListener('click', startNewGame);
  document.addEventListener('keydown', (event) => {
    // Correct the arrow key mapping for tile movement
    if (event.key === 'ArrowUp') handleTileMovement(0); // Up
    else if (event.key === 'ArrowRight') handleTileMovement(1); // Right
    else if (event.key === 'ArrowDown') handleTileMovement(2); // Down
    else if (event.key === 'ArrowLeft') handleTileMovement(3); // Left
  });
});
