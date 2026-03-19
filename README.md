# SousChef

## Overview
My final project for CS50’s Web Programming with Python and JavaScript.

SousChef is an online recipe book built on the Django framework with additional front-end features written in JavaScript.

## Features
With a clean, minimalist layout and a fully responsive design, SousChef lets you:
- Create and edit your own recipes
- Browse recipes shared by other users
- Save favourites to your personal collection
- Track ingredients in your Pantry with nutritional info powered by the Spoonacular API
- Fully responsive design. Works on desktop, tablet, and mobile

## Prerequisites
- Python 3.x
- A free API key from Spoonacular: You can sign up for a free plan here: https://spoonacular.com/food-api

## Setup

**1. Clone the repository**

    
    git clone https://github.com/mcgooz/SousChef.git
    cd capstone

**2. Set up environment variables**  
Create a .env file in the root directory and add your Spoonacular API key:

    API_KEY = your_api_key_here

**3. Install dependencies**

    pip install -r requirements.txt

**4. Set up the database**

    python manage.py makemigrations
    python manage.py migrate

**5. Run the server**

    python manage.py runserver

**6. Open the app**
Visit `http://127.0.0.1:8000/` in your browser or click the link in the terminal.