# CS50’s Web Programming with Python and JavaScript - Final Project

## SousChef
SousChef is a recipe book webapp built on the Django framework with addtional front-end functionality written in JavaScript.
It utilises the Spoonacular API which gives us access to a large database of ingredients along with their nutritional values.

With a clean, minimalistic layout and responsive design, it provides users with the ability to store their recipes, view others' and collect a list of favourites.
In addition, it also comprises a "Pantry" section, allowing users to keep track of the ingredients they have at home and view relevant nutritional information.

### Distinctiveness and Complexity
Athough it shares some common, necessary elements, such as user profiles and favourites, this project is conceptually distinct from the other projects in the course.
It's primary function is to save, view and share recipes, as well as provide some basic nutritional information of ingredients.

#### API

This project utilises a third-party API, Spoonacular, to search for and retrieve ingredients, giving users access to a large, maintained database and also ensuring a degree of consistency across the app, since users can't simply create ingredients themselves. Were that the case, these ingredients wouldn't have the necessary nutritional information and there would also be a risk of typos and the potential to fill the database with duplicates and so on (*see additional info for more on this).

#### Django features

The desgin and scope of the project also goes beyond what was covered in previous projects. Some are subtle details, such as automatically creating a user dashboard and pantry on registering, or using custom template filters, while others required digging deep into the documentation.

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
Since there were a number of linked models, I used `InlineModelAdmin` objects so backend management was easier.

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

Some other features used that contribute towards the project's complexity are:
 - context processors, to pass the date to all templates
 - `JSONField` model to store ingredient details
 - custom template filters

#### JavaScript

My weakest point going into this project was JavaScript. Nevertheless, my intention was to implement a smooth user-experience and try to approximate a professional design, for which JS would be hugely important. As the project grew, so did my understanding of the language (as well as scripts.js) and I think that shows as the functionality gets more complex and, perhaps, less convoluted.

##### Cropper.js

In order to allow users to crop images (and to ensure a uniform rendering of images), I made use of the 3rd-party library, Cropper.js.

##### Horizontal Scroller

I implemented a scrolling feature for the recipes page, rather than presenting the whole list at once, so that users could scroll or swipe through recipes.

##### Search suggestions

When the user searches for an ingredient, the API returns a set of suggested results. I used JS on the front end to display these suggestions, in a style consistent with the rest of the site, and then, on selection, passed that ingredient to the back end to be stored. Additionally, I used `debounceTimer;` to avoid API calls after every keystroke.

##### Adding Recipes
The most challenging (and frustrating) part of the JS side, was implementing a satisfactory UI for adding ingredients and steps to recipes. This was particularly difficult for adding steps, as they had to be added and removed in order to stay in sync with the formset.

##### AJAX
The app makes use of several AJAX requests to avoid reloading the page when passing data back and forth or when the user wants to make a change, for example, uploading a profile picture.


#### Python
I've used several 3rd-party libraries in the app:
- dotenv to save the API key outside of the main files and import it from the .env file
- pillow is required for image processing
- requests to interact with the Spoonacular API
- titlecase to automatically format titles correctly

and some that are included in with Python:
- decimal
- json
- random
- os

Additionally, I have created several functions to deal with the adding of ingredients to the user's pantry, specifically updating amounts and the corresponing units. These functions, among other helper functions, can be found in the utils.py file. 

#### CSS
Lastly, I have taken care to give the website a distinct, slick aesthetic, with fully responsive design. This was acheived using Bootstrap in addition to custom css.


### Files
What’s contained in each file you created.

### How to Run
How to run your application.

### Additional info
*Admittedly, there are, of course, edge cases in which a user may need to add an
ingredient that doesn't exist in the database. Should there not be a suitable approximation available, there currently isn't a workaround but I hope to be able to address that in future updates.
