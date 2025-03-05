# CS50’s Web Programming with Python and JavaScript - Final Project
## SousChef

#### YouTube link: https://www.youtube.com/watch?v=rkyRg7OpAX0

## Overview
SousChef is an online recipe book built on the Django framework with additional front-end functionality written in JavaScript. 
With a clean, minimalist layout and a fully responsive design, SousChef lets users create their own recipes, browse those of others and add recipes to their list of favourites. 
The app also includes a "Pantry" section, allowing users to keep track of the ingredients they have at home and view relevant nutritional information.


## Distinctiveness and Complexity
SousChef distinguishes itself from the previous projects in both concept and scope. It utilises more Django features, has deeper JavaScript integration, and solves more complex challenges. The app incorporates 10 models, dynamic AJAX functionality, image editing via Cropper.js, and third-party API integration (Spoonacular). It handles detailed, multi-step user inputs using formsets and management forms. It's also designed with efficiency in mind, using memcache to reduce reliance on API calls and Q() object filtering for flexible searches.

Beyond backend improvements, SousChef introduces new, interactive front-end features and enhancements: real-time AJAX updates for image previewing and search suggestions, horizontal scrolling with touchscreen support, and a fully responsive UI with custom CSS and Bootstrap styling.

Below, I will further describe how these features set the project apart and contribute to its complexity and distinctiveness:

<details>
    <summary><strong>Third-party API</strong></summary>

##### Spoonacular Ingredient API
While Commerce let users create a listing by entering all the details manually, this project instead utilises a third-party API, Spoonacular, to search for and retrieve ingredients and nutritional data, both when adding them to a recipe and also when adding them to the user's pantry. This not only gives users access to a vast, well-maintained repository of ingredients and accurate nutritional data, but also ensures a degree of consistency across the app and avoids the introduction of errors, duplicates, and inconsistencies.
</details>

<details>
    <summary><strong>Django Features</strong></summary>

##### Cache
In order to avoid repeatedly making API requests for the same search, I implemented basic caching. As this was mostly to save precious API calls while in a development environment, I opted for Django's *Local-memory caching*. For a production environment, a more advanced caching solution would most likely be required, however.

I first defined the type of cache (`LocMemCache`) in settings.py:
```
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-churro",
    }
}
```
And then integrated it into the API searches:
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
```
def detailed_search(id):
    details = cache.get(f"item_details_{id}")
    if details:
        print("DETAILS RETRIEVED FROM CACHE")

    else:
        # search via API

    return details
```

##### Models and Forms
A total of ten models were used in this project. I also made use of formsets to allow for more advanced, interlinked data input. By defining custom widgets, I was able to customise and adapt the form elements for a more intuitive UX that matched the project's overall aesthetic.
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
Since lots of model data was connected via Django's relational fields, such as `ForeignKey` and `ManyToManyField`, I also used `InlineModelAdmin` objects so backend management via Django admin would be easier and more intuitive.

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

##### Q Objects
For the search function on the homepage, I wanted to allow users to find recipes by searching for either the title of a recipe or a consituent ingredient (or both). 
To do this, I created a search function using `Q()` objects and the OR operator (`|`) to recognise the search term ('word'), case-insensitively, in both recipe titles and recipe ingredients. To ensure no unnecessary repetition, I also utilised the `distinct()`method.
```
from django.db.models import Q

def home_search(request):    
    if 'word' in request.GET:
        word = request.GET.get('word')
        recipes = Recipe.objects.filter(
            Q(title__icontains=word) | Q(ingredients__name__icontains=word)
            ).values('title', 'id').distinct()
        recipe_result = list(recipes)

        return JsonResponse({"recipe_result": recipe_result})

```
##### Allowed Hosts
To test the project on other devices on my home network, I added the necessary ip addresses to `ALLOWED_HOSTS = []` in `settings.py`.


##### Other
In addition to the above, I also researched and implemented other Django features not specifically required in previous projects:
 - context processors to pass the date to all templates
 - custom template filters
 - `JSONField` model to store ingredient details
</details>

<details>
    <summary><strong>JavaScript</strong></summary>

My intention for this project was to implement a smooth user-experience and try to approximate a professional design, going beyond what was covered in previous projects. Despite having some previous experience with JavaScript, I still considered it my weakest point. Therefore, I decided to stick to vanilla JS so that I could refine my skills and understanding before progressing to React or another framework.

All my JavaScript is contained in a single file, `scripts.js`. Some of the more distinctive and complex parts are detailed as follows:

##### Cropper.js
In order to allow users to crop images (and to ensure a uniform rendering of images), I made use of the 3rd-party library, `Cropper.js`. Most default cropper parameters remained unchanged except for:
- `viewMode: 2` ensured the image fit within the container
- `aspectRatio: 1` maintained a 1:1 aspect ratio, i.e., always square
- `autoCropArea: 1` defined the initial crop area as 100%
- `responsive: true` ensured that the cropper would resize responsively

The cropper overaly is contained within a Bootstrap modal, allowing users to preview and fine-tune images before submitting, which seemed to be a great option with regard to UX.

To save the image, either as a preview in the form field to later be submitted, or directly via AJAX, I needed to explore the process of converting the cropped image, creating a preview, and also replacing the initial input with the cropped version so that only this version would be saved to the database. Fortunately, most of this, including `toBlob`, was helpfully outlined in the docs for cropper.js here: https://github.com/fengyuanchen/cropperjs/blob/v1/README.md#methods, under `getCroppedCanvas`.

##### Search suggestions
When the user searches for an ingredient, the API returns a set of suggested results. I used JavaScript to display these suggestions on the front end in a style consistent with the rest of the site, and then, on selection, pass that ingredient to the back end via AJAX to be stored. Additionally, I used `debounceTimer;` to avoid API calls after every keystroke.

##### Adding Recipes
The most challenging (and frustrating) part of the JavaScript part, was implementing a satisfactory UI for adding ingredients and steps to recipes. This was particularly difficult for steps, as they each had to be added and removed in order to stay in sync with the formset numbers.

As these sections both relied on formsets, it was important to index each new element in the corresponding `formset.management_form` in the template.

##### Scroller
I wanted to explore options for a unique and interesting UI to browse recipes, so I implemented a horizontal scrolling system with multiple input methods for smooth navigation. Designed to be completely responsive, it includes several navigation options:
- Buttons: Users can click left/right buttons on the page to scroll through the recipes.
- Mouse wheel & Touchpad: The script allows horizontal scrolling via the scroll wheel or touchpad gestures.
- Touchscreen: Users can swipe to scroll, with adjustable sensitivity for a more fluid experience.

</details>

<details>
    <summary><strong>Python</strong></summary>

I made use of Python's built-in capabilities alongside several third-party libraries to enhance functionality and efficiency.

Third-Party:
- dotenv to securely load the API key from the .env file, keeping it separate from the main codebase 
- pillow is required for image processing
- requests to interact with the Spoonacular API
- titlecase to automatically format titles correctly

Built-in:
- decimal ensured precision in ingredient measurements and prevented issues with floating-point numbers.
- json for managing data
- random to generate random recipes on the front page
- os 

Additionally, I created several helper functions to deal with operations such as API calls, adding ingredients to the user's pantry - specifically, correctly updating amounts and the corresponding units. These helper functions, among others, can be found in the `utils.py` file.

</details>

<details>
    <summary><strong>HTML</strong></summary>
The project has a layout.html file which references the necessary scripts and CSS for all pages. From there, I have structured the different pages according to their function, ensuring that the design is consistent and works across different screen sizes. This includes the use of several Bootstrap features, such as modals and cards etc. I have also made use of comments to allow for easier navigation through the sections on the page.
</details>

<details>
    <summary><strong>CSS</strong></summary>
Lastly, I have taken care to give the website a distinct, slick aesthetic, with fully responsive design. This was achieved using Bootstrap in addition to custom CSS on top.
</details>

## Files

#### Directory Tree
<details>
<summary>capstone/</summary>


```  
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
</details>  

#### File Breakdown and Contributions

<details>
    <summary>/capstone/</summary>

##### `settings.py`

- Modified `ALLOWED_HOSTS` so that I could test the app on other devices on my home network.   
- Added the app "souschef" to `INSTALLED_APPS`.   
- Within `TEMPLATES`, added `"souschef.context_processors.date"` to allow me to pass the date to any template.   
- As detailed above, set up the cache in `CACHES`.
- Defined a custom user model via `AUTH_USER_MODEL = "souschef.User"`
- Configured media settings to allow image uploads:  
`MEDIA_URL = '/media/'`  
`MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`

##### `urls.py`

- Set up routing for the admin interface and app URLs
```
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("souschef.urls"))
]
```
</details>

<details>
    <summary>/media/</summary>
The files contained in the two sub-folders are the user-uploaded images.

</details>  

<details>
<summary>/souschef/</summary>
<details>      
<summary>/static/</summary>  

##### `fonts/`
This folder contains the woff/woff2 files of the custom font, referenced in `styles.css`.

##### `images/`
This is where all the default images, backgrounds and logos are stored.

##### `static.js` 
All of the JavaScript that I have written is contained in this file. Additional JS functionality is loaded from Cropper.js and Bootstrap via `<script>` tags in the templates.

##### `styles.css`
Contains all additional CSS that is not part of Bootstrap or Cropper.js.
         
</details>

<details>
<summary>/templates/souschef/</summary>  

##### `add_recipe.html`
The html template for adding a recipe.

##### `index.html`
The home page, which includes a recipe search and also displays a random recipe from the DB.

##### `ingredient.html`
On selecting an ingredient, this page will display its nutritional values.

##### `layout.html`
This sets the layout of each template and contains the navbar structure, as well as importing any required CSS or scripts to each page.

##### `login.html`
The page where users log in.

##### `pantry.html`
The template where users can add and remove ingredients from their virtual pantry.

##### `recipe.html`
This page shows the full recipe, with an image, ingredients, description, steps and the creator.

##### `recipes.html`
An overview of all recipes currently saved in the DB.

##### `register.html`
The page where users can create their profile.

##### `user_dashboard.html`
The user's personal dashboard where they can update their profile picture, recipe images and delete recipes they have created.
</details>

<details>
<summary>/templatetags/</summary>  

##### `__init__.py`
Empty, although required to initialise `custom_filters.py`

##### `custom_filters.py`
Created to be able to use custom filters in the templates.
The included `custom_floatformat(value)` helps to make decimal values cleaner by removing unecessary zeros.
</details>


##### `add_recipe_view.py`
To simplify `views.py`, I moved the logic for adding recipes via GET and POST request into this file and imported the corresponding functions back into `views.py`.
The GET function passes the necessary forms and formsets to the template.
The POST function validates the forms, checks that the recipe title is unique, and saves the data to the corresponding, interlinked models.

##### `admin.py`
This is used to configure the Django admin interface. The `User` and `Unit` models are registered with the default settings, while the rest rely on custom configurations, using inline models for an easy-to-manage, intuitive layout.

##### `apps.py`
Auto-generated by Django.

##### `context_processors.py`
This file retrieves the date using the *datetime* library, returns it as a context variable so that it can be accessed in any template across the project.

##### `forms.py`
Where all the app's forms and formsets are defined and customised.
- `UserDashboardForm` - update the user's profile picture
- `NewRecipeForm` - add new recipes
- `IngredientForm` - add ingredients
- `PantryIngredientForm` - add pantry ingredients

and the formsets:
- `StepFormSet` - add recipe steps
- `IngredientPerRecipeFormSet` - add different ingredients to a recipe

##### `models.py`
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

##### `pantry_view.py`
Similar to the add recipe view, I moved the pantry view to a separate file so that it was easier to manage.
The GET function handles the API search and passing the relevant forms to the template.
The POST function validates the forms, checks whether an ingredient exists in the DB as well as in the user's pantry and then, if necessary, calls a helper function to update the quantity and unit.
Finally, we save the item to the user's pantry via the `PantryIngredient` model.

##### `urls.py`
Defines all the url patterns for the app and includes the media root path.

##### `utils.py`
This file contains helper functions for searching via the Spoonacular API, caching searches, and managing ingredient data in the database. Additionally, there are functions for quantity and unit conversions (e.g., grams to kilograms) and updating items in the pantry.

##### `views.py`
This contains all the other functions used to render templates, process GET and POST requests and handle AJAX requests. For pages only meant for logged-in users, the `@login_required` decorator is used in addition to checks in the relevant templates.
</details>

##### `.env`
Contains the API key and keeps it separate from the rest of the codebase. Requires `dotenv` to import the key to `utils.py`.

##### `.gitignore`
This ensures that only the necessary files are saved, comitted and pushed via Git.

##### `db.sqlite3`
The SQLite database file used to store all of the model data.

##### `README.md`
A detailed write-up of the project.

##### `requirements.txt`
Lists all the Python packages that should be installed for the web app to run.

## How to Run
Note that the API used in this project requires an API key that is linked to a Spoonacular account. There is a free option that can be found here: https://spoonacular.com/food-api  

Once you have an API key, add it to the .env file:
```
API_KEY = ADDYOURAPIKEYHERE
```

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
Ingredients API and limitations - I decided not to allow users to create their own ingredients as these entries wouldn't have the related nutritional information and could introduce the previously mentioned inconsistencies. Admittedly, there are edge cases in which a user may need to add an ingredient that doesn't exist in the database. More often than not, there is suitable approximation available, which can be mentioned in the description or steps.

There are still some other features that I would lkie to implement in future updates and I would like to optimise certain parts of the code and logic. 
Some of these future updates would include:
- Edit Recipes - Probably the most glaring omission. There were two issues that I kept running into here. First, keeping the `StepFormSet` in sync with the cloned rows when editing a recipe. Second, validating and saving the edits to the recipe instance.
- Rewrite the logic for saving ingredients to the DB. Currently, an ingredient is saved to the DB when selected from the suggestions, not when saved via a form. This was to make it easier to manage ingredients across several models and formsets, and it made sense at the time, but I definitely think there is room for improvement.
- Additional images for each recipe, potentially linked to steps.
- Linked pantry - when visiting a recipe page, the app will tell you which ingredients you already have in the pantry and which are missing. Additionally, a feature that allows you to mark the recipe as "made", would remove that quantity of specified ingredients from your pantry.
- Filter recipes by category etc. on the recipes page.
- Dark mode/high contrast mode - On some screens, with night light enabled, the colours can be slightly hard on the eyes. It could do with some tweaks and I'd like to explore a dark mode / high contrast option.
- Bootstrap Toasts - I'd like to use toast notifications for certain completed operations, such as updating a picture successfully.
- Improved horizontal scroll on mobile - currently it isn't as responsive as it could be.