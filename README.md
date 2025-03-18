# SousChef

## Overview
This was my final project for CS50’s Web Programming with Python and JavaScript.

SousChef is an online recipe book built on the Django framework with additional front-end features written in JavaScript.
With a clean, minimalist layout and a fully responsive design, SousChef lets users create their own recipes, browse those of others, and add recipes to their list of favourites. 
The app also includes a "Pantry" section, allowing users to keep track of the ingredients they have at home and view relevant nutritional information.

## How to Run
Note that the API used in this project requires an API key associated with a Spoonacular account. You can sign up for a free plan here: https://spoonacular.com/food-api  

- Once you have an API key, add it to the .env file:
    ```
    API_KEY = ADDYOURAPIKEYHERE
    ```

- Install the necessary libraries, as listed in requirements.txt, to your environment.

- Before running the server, you'll need to set up the database: 

    - In the terminal run:  
    `python manage.py makemigrations`

    - followed by:  
    `python manage.py migrate`  

    - To start the server, run:  
    `python manage.py runserver`  

    - Then, visit this URL or click the link in the terminal to open the app:  
    `http://127.0.0.1:8000/`
