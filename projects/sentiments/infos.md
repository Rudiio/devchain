# Project Informations

## Request
A Sentiment analysis web application. It should take as input some text from the user and output if the input is negative, positive or neutral with the corresponding percentage. The backend should use python and fastapi to create a REST API. The app should include an endpoint to analyze the sentiment of a text via Roberta model used directly via huggingface/transformers. The application should include an app.py file that directly starts the FastAPI app via uvicorn. The backend should serve/render directly the front-end application built with Html, javascript and styled with tailwindcss. The UI should have a similar style as the UI from ChatGPT. The title of the application should be styled in big at the top-center, the text area should be in the bottom center and the results should appear dynamically in the center of the window.

## Name
Sentimint Analytica

## Description
Sentimint Analytica is a web application designed to provide sentiment analysis of user-inputted text through a clean and intuitive interface reminiscent of ChatGPT's UI. The application's backend, developed in Python using FastAPI, will serve the front-end directly and handle REST API requests, including an endpoint that utilizes the RoBERTa model from the Hugging Face `transformers` library for sentiment analysis. The front-end will be accessible via the root URL and will feature a text area for users to input their text, a submit button to initiate analysis, and a dynamic display area for the results, which will indicate whether the sentiment is positive, negative, or neutral, along with a corresponding percentage. The UI will be styled with TailwindCSS, ensuring responsiveness and a familiar aesthetic, with the application's title prominently displayed at the top-center of the page. The `app.py` file will be responsible for initializing and starting the FastAPI app with Uvicorn. Error handling will be a crucial aspect, providing users with clear feedback in case of invalid input or server issues. The overall goal is to deliver a user-friendly sentiment analysis tool that is both reliable and easy to use across desktop and mobile devices.

