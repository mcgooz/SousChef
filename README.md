# CS50’s Web Programming with Python and JavaScript - Final Project

## SousChef
SousChef is a recipe book webapp built on the Django framework with addtional front-end functionality written in JavaScript.
It utilises the Spoonacular API which gives us access to a large database of ingredients along with their nutritional values.

With a clean, minimalistic layout and responsive design, it provides users with the ability to store their recipes, view others' and collect a list of favourites.
In addition, it also comprises a "Pantry" section, allowing users to keep track of the ingredients they have at home and view relevant nutritional information.

### Distinctiveness and Complexity
Athough it shares some common elements, such as user profiles and favourites, this project is conceptually distinct from the other projects in the course.
Its primary function is to save, view and share recipes, as well as provide some basic nutritional information of ingredients. 
Its design and scope go beyond what was required for each individual project and the goal was to encapsulate the techniques and principles taught across the whole course and, hopefully, go a bit further.

#### API
This project utilises a third-party API, Spoonacular, to search for and retrieve ingredients, giving users access to a large, well-maintained database and also ensuring a degree of consistency across the app, since users can't simply create ingredients themselves. Were that the case, these ingredients wouldn't have the related nutritional information and there would also be a risk of typos and the potential to fill the database with duplicates and so on (*see additional info for more on this).

#### Django features
##### Cache
In order to avoid repeatedly making API requests for the same search, I implemented basic local-memory caching. First, by adding it in settings.py:
```
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-churro",
    }
}
```
And then integrating it into the API search:
```
def item_search(s):
    safe = s.replace(" ", "_")
    results = cache.get(f"item_search_{safe}")
    if results:
        print("SEARCH RETRIEVED FROM CACHE")

    else: 
        # search via API

    return results
```

##### Models and Forms
A total of ten models were used in this project. To allow for more advanced, detailed forms, I made use of formsets, defining custom widgets where necessary:
```
from django.forms import inlineformset_factory

IngredientPerRecipeFormSet = inlineformset_factory(
    Recipe,
    IngredientPerRecipe,
    can_delete=True,
    fields = ['ingredient', 'amount', 'unit'],
    widgets = {
        "id": HiddenInput(attrs={"class": "id-input"}),
        "ingredient": HiddenInput(attrs={"required": "required", "class": "form-control search-box-id"}),
        "amount": NumberInput(attrs={"required": "required", "class": "form-control amount-input"}),
        "unit": Select(attrs={"required": "required", "class": "form-control form-select unit-input"}),
    },
)
```
Since there were a number of linked models, I used `InlineModelAdmin` objects so backend management via Django admin would be easier and more intuitive.

##### Image Uploads
In Project 2, Commerce, we used URLs to link to images for items. In SousChef, I integrated image uploads directly into the app. 
For this, it was necessary to configure the media root in settings.py and urls.py and use `ImageField` in the models and `ClearableFileInput` in the corresponding forms.
```
settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

======

urls.py

+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

##### Other
Some other features used:
 - context processors, to pass the date to all templates
 - custom template filters
 - `JSONField` model to store ingredient details
 - `Q()` object used for retrieving recipes when searching with both recipe names and constituent ingredients

#### JavaScript
My weakest point going into this project was JavaScript. Nevertheless, my intention was to implement a smooth user-experience and try to approximate a professional design, for which JS would be hugely important. As the project grew, so did my understanding of the language (as well as scripts.js) and I think that shows as the functionality gets more complex and, perhaps, less convoluted.

##### Cropper.js
In order to allow users to crop images (and to ensure a uniform rendering of images), I made use of the 3rd-party library, Cropper.js.

##### Search suggestions
When the user searches for an ingredient, the API returns a set of suggested results. I used JS on the front end to display these suggestions, in a style consistent with the rest of the site, and then, on selection, passed that ingredient to the back end to be stored. Additionally, I used `debounceTimer;` to avoid API calls after every keystroke.

##### Adding Recipes
The most challenging (and frustrating) part of the JS side, was implementing a satisfactory UI for adding ingredients and steps to recipes. This was particularly difficult for the steps part, as they each had to be added and removed in order to stay in sync with the formset numbers.

##### AJAX
The app makes use of several AJAX requests to avoid reloading the page when passing data back and forth or when the user wants to make a change, for example, uploading a profile picture.


#### Python
I've used several 3rd-party libraries in the project:
- dotenv to import the API key from outside of the main files from the .env file
- pillow is required for image processing
- requests to interact with the Spoonacular API
- titlecase to automatically format titles correctly

and some that are included in with Python:
- decimal
- json
- random
- os

Additionally, I have created several helper functions to deal with operations such as API calls, adding ingredients to the user's pantry - specifically, correctly updating amounts and the corresponing units. These helper functions, among others, can be found in the utils.py file.

#### HTML
The project has a layout.html file which references the necessary scripts and css for all pages. From there, I have structured the different pages according to their function, ensuring that the design is consistent and works across different screen sizes. I have also made use of comments to allow for easier navigation through the sections on the page.

#### CSS
Lastly, I have taken care to give the website a distinct, slick aesthetic, with fully responsive design. This was acheived using Bootstrap in addition to custom css on top.


### Files
The project is structured as follows:
``` 
capstone/  
├── capstone/  
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/
│   ├── profile_pics/
│   └── recipe_pics/
├── souschef/
│   ├── static/
│   │   ├── fonts/
│   │   ├── images/
│   │   ├── scripts.js
│   │   └── styles.css
│   ├── templates/
│   │   └── souschef/
│   │   │   ├── add_recipe.html
│   │   │   ├── index.html
│   │   │   ├── ingredient.html
│   │   │   ├── layout.html
│   │   │   ├── login.html
│   │   │   ├── pantry.html
│   │   │   ├── recipe.html
│   │   │   ├── recipes.html
│   │   │   ├── register.html
│   │   │   └── user_dashboard.html
│   └── templatetags/
│   │   ├── __init__.py
│   │   └── custom_filters.py
│   ├── __init__.py
│   ├── add_recipe_view.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── pantry_view.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```
Each of the files that I created are detailed as follows:

#### Static Files
##### scripts.js
All of the JavaScript that I have written is contained in this file. Other JS functionality is loaded directly from Cropper.js and Bootstrap.

##### styles.css
Contains all additional css that is not part of Bootstrap or Cropper.js.

#### Templates
##### add_recipe.html
The html template for adding a recipe.

##### index.html
The home page, which includes a recipe search and shows a random recipe from the DB.

##### ingredient.html
On selecting an ingredient, this page will display its nutritional values.

##### layout.html
This sets the layout of each template and contains the navbar structure, as well as importing any required css or scripts to each page.

##### login.html
The page where users log in.

##### pantry.html
The template where users can add and remove ingredients from their virtual pantry.

##### recipe.html
This page shows the full recipe, with an image, ingredients, description, steps and the creator.

##### recipes.html
An overview of all recipes currently saved in the DB.

##### register.html
The page where users can create their profile.

##### user_dashboard.html
The user's personal dashboard where they can update their profile picure, recipe images and delete recipes they have created.


#### Template Tags
##### \_\_init__.py and custom_filters.py
These files were created to be able to use custom filters in the templates.


#### Python Files
##### add_recipe_view.py
Since the add recipe view was becoming long, I decided to create a dedicated file for it and then import the functions back into views.py

##### context_processors.py
This file is used to pass the date to each template, without having to pass it as context in every view.

##### forms.py
The file where all the app's forms are defined and customised. This includes the inline formsets. The forms allow users to:
- update the user profile picture
- add new recipes
- add ingredients
- add pantry ingredients

and the formsets to:
- add recipe steps
- add different ingredients to a recipe

##### models.py
Here we find the models used in the app:
- `UserDashboard` stores the username, creation date and the profile picture
- `Pantry` is linked to the user and is referred to by the `PantryIngredient` model
- `Unit` is a predefined list of units
- `Ingredient` stores the ingredient name, API ID and details in JSON format
- `Recipe` contains the full details of a recipe
- `IngredientPerRecipe`stores the ingredients for a particular recipe
- `PantryIngredient`stores the ingredients in a particular user's pantry
- `Step`is the model for saving steps for a particular recipe
- `Favourite` keeps a record of which recipes have been favourited by a user

##### pantry_view.py
Similar to the add recipe view, I moved the pantry view to a separate file so that it was easier to manage.

##### urls.py
Defines the url patterns for the app and includes the media root path.

##### utils.py
This file contains several helper functions including API requests and caching, saving or retrieving an ingredient from the DB, generating table data for the pantry, saving ingredients to a recipe and dealing with conversions between units, e.g., grams to kilograms.

##### views.py
This contains all the other functions used to render templates, process GET and POST requests and handle AJAX requests. For pages only meant for logged-in users, the `@login_required` decorator is used in addition to checks in the relevant templates.

#### Other Files
##### .env
Contains the API key and keeps it separate from the rest of the code. Requires dotenv to import the key to utils.py

##### .gitignore
This ensures that only the necessary files are saved, comitted and pushed with Git.

##### README.md
A detailed write-up of the project

##### requirements.txt
Lists all the Python packages that should be installed for the web app to run.

### How to Run
Note that the API used in this project requires an API key that is linked to a Spoonacular account. There is a free option that can be found here: https://spoonacular.com/food-api  

Your environment should have the necessary libraries installed, as listed in requirements.txt.

Before running the server, you'll need to set up the database: 

In the terminal run:  
`python manage.py makemigrations`

followed by:  
`python manage.py migrate`  

To start the server, run:  
`python manage.py runserver`  

Then, visit this URL to open the app:  
`http://127.0.0.1:8000/`


### Additional info
*Ingredients API and limitations - Admittedly, there are edge cases in which a user may need to add an ingredient that doesn't exist in the database. More often than not, there is suitable approximation available, which can be mentioned in the description or steps.

There are still some other features that I had hoped to implement, but I eventually decided that, as the project was already becoming quite large, I would leave them for future updates. In addition, I would like to optimise certain parts of the code and logic. 
Some of these future plans would include:
- Rewrite the logic for saving ingredients to the DB. Currently, an ingredient is saved to the DB when selected from the suggestions, not when saved via a form. This was to make it easier to manage ingredients across several models and formsets, and it made sense at the time, but I definitely think there is room for improvement.
- Additional images for each recipe, potentially linked to steps.
- Edit Recipes - I spent a significant amount of time trying to get the the `StepFormSet`to stay in sync with the cloned rows when editing a recipe. Ultimately, I decided to leave it out so, for now, you can only replace the image or delete the recipe.
- Linked pantry - when visiting a recipe page, the app will tell you which ingredients you already have in the pantry and which are missing. Additionally, a feature that allows you to mark the recipe as "made", would remove that quantity of specified ingredients from your pantry.
- Filter recipes by category etc. on the recipes page.
- Dark mode/high contrast mode - On some screens, with night light enabled, the colours can be slightly hard on the eyes. It could do with some tweaks and I'd like to explore a dark mode / high contrast option.
- Bootstrap Toasts - I'd like to use toast notifications for certain completed operations, such as updating a picture successfully.
- Improved horizontal scroll on mobile - currently it isn't as responsive as it could be.