document.addEventListener("DOMContentLoaded", function() {

    // Main Search
    let searchInput = document.getElementById('homeSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            let query = this.value;
            homeSuggestions.innerHTML = '';

            if (query === '') {
                return;

            } else {
                fetch(`home_search/?word=${query}`)
                .then(response => response.json())
                .then(data => {
                    const recipeResult = data.recipe_result;
                    const recipeItems = recipeResult.map(item => ({id: item.id, title: item.title }));
                    // console.log('recipeItems', recipeItems);

                    const homeSuggestions = document.getElementById('homeSuggestions');
                    
                    function createListItem(text, id) {
                        const listItem = document.createElement('li');
                        listItem.className = 'list-group-item';
                        listItem.textContent = text;
                        listItem.dataset.id = id;
                        homeSuggestions.appendChild(listItem);
                        return listItem;
                    }
                    
                    if (recipeItems.length === 0) {
                        createListItem('No results found');

                    } else {
                        recipeItems.forEach(item => {
                            const listItem = createListItem(`${item.title}`, item.id);

                            listItem.addEventListener('click', function() {
                                const itemId = listItem.dataset.id;
                                window.location.href = `/recipe/${itemId}`;
                            });
                        });
                    }
                });
            }
        });
    }

    // Search via API and autocomplete
    const searchBoxes = document.querySelectorAll('.search-box');
    const suggestionsContainers = document.querySelectorAll('.suggestions');
    
    if (searchBoxes && suggestionsContainers) {
        let suggestions = [];
        let debounceTimer; // Prevent API calls after each keystroke

        // Detect input in search box
        searchBoxes.forEach((searchBox, index) => {
            const suggestionsContainer = suggestionsContainers[index];
            handleInput(searchBox, suggestionsContainer)

        });

        function handleInput(searchBox, suggestionsContainer) {
            searchBox.addEventListener('input', function() {
                const query = this.value;
                this.value = this.value.replace(/[0-9]/g, '');

                if (query.length >= 2) {
                    clearTimeout(debounceTimer); // Clear timer then restart at 500ms

                    debounceTimer = setTimeout(function() {
                        fetchSuggestions(query, suggestionsContainer, searchBox);
                        searchBox.classList.add('autocomplete-active');
                    }, 500);
                    
                } else {
                    clearTimeout(debounceTimer);
                    clearContent(suggestionsContainer);
                    searchBox.classList.remove('autocomplete-active');
                    // console.log('Clearing suggestions');
                }
            });
        }
        

        // Fetch suggestions
        function fetchSuggestions(query, suggestionsContainer, searchBox) {
            if (query.length < 2) {
                return;
            }

            fetch(`/pantry?query=${query}`)
            .then(response => response.json())
            .then(data => {
                const details = [];
                const results = data.results;

                for (let i = 0; i < results.length; i++) {
                    details.push({name: results[i].name, id: results[i].id});
                }
                
                displaySuggestions(details, suggestionsContainer, searchBox);
                // console.log(details)
            })
            .catch(error => {
                // console.error('Error fetching suggestions:', error);
            });
        }

        // Display suggestions
        function displaySuggestions(details, suggestionsContainer, searchBox) {
            suggestionsContainer.innerHTML = '';

            if (details.length === 0) {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = 'No results found';
                suggestionsContainer.appendChild(li);

            } else {

                details.forEach(item => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item';
                    li.textContent = item.name;
                    li.setAttribute('data-name', item.name);
                    li.setAttribute('data-id', item.id);
                    suggestionsContainer.appendChild(li);

                    li.addEventListener('click', function() {
                        const itemName = this.getAttribute('data-name');
                        const itemId = this.getAttribute('data-id');
                        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                        
                        
                        fetch('/ingredient_details/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrfToken
                            },
                            
                            body: JSON.stringify({ 
                                id: itemId,
                                name: itemName
                            })

                        })
                        // Add item to field
                        .then(response => response.json())
                        .then(data => {
                            const ingredientId = data.details.ingredient.id;
                            // console.log('Item ID', itemId)
                            // console.log('Ingredient ID:', ingredientId);

                            if (!itemName) {
                                alert("Please select an item from the list");

                            } else {
                                
                                searchBox.value = itemName;
                                const itemInput = document.getElementById('ingredientId');
                                itemInput.value = itemId;

                                const itemObjectID = this.closest('tr')?.querySelector('.search-box-id');
                                
                                if (itemObjectID) {
                                    itemObjectID.value = ingredientId;
                                }

                                clearContent(suggestionsContainer);
                            }
                        })
                    })
                })
            }
        }
    }

    // Scroller
    const scroller = document.getElementById('scroller')
    if (scroller) {

        // Buttons
        const scrollLeftButton = document.getElementById('scrollLeft');
        const scrollRightButton = document.getElementById('scrollRight');
        const scrollAmount = 200;

        scrollLeftButton.addEventListener("click", () => {
            scroller.scrollBy({ left: -scrollAmount, behavior: "smooth"});
        });

        scrollRightButton.addEventListener("click", () => {
            scroller.scrollBy({ left: scrollAmount, behavior: "smooth"});
        });


        // Mouse wheel or touchpad
        scroller.addEventListener('wheel', (event) => {
            event.preventDefault();
            scroller.scrollBy({
            left: event.deltaY +event.deltaX < 0 ? -25 : 25,
            });
        });

        // Touchscreen
        let isTouching = false;
        let startX = 0;
        let scrollLeft = 0;
    
        scroller.addEventListener('touchstart', (event) => {
            isTouching = true;
            startX = event.touches[0].pageX - scroller.offsetLeft;
            scrollLeft = scroller.scrollLeft;
        });
    
        scroller.addEventListener('touchmove', (event) => {
            if (!isTouching) return;
            event.preventDefault();
            const x = event.touches[0].pageX - scroller.offsetLeft;
            const walk = (x - startX) * -1;
            scroller.scrollLeft = scrollLeft + walk;
        });
    
        scroller.addEventListener('touchend', () => {
            isTouching = false;
        });
    }

    // Update recipe ingredeints
    const recipeIngredientInput = document.querySelector('#ingredient-formset');
    if (recipeIngredientInput) {
        
        let counter = 1;
        function addRowEventListener(button) {
            button.addEventListener('click', function(event) {
                event.preventDefault();
                // console.log("clicked");
        
                const formRow = document.getElementById('ingredientRow');
                const newRow = formRow.cloneNode(true);

                newRow.querySelectorAll('.id-input').forEach((input) => {
                    input.name = `ingredientperrecipe_set-${counter}-id`;
                    input.id = `ingredientperrecipe_set-${counter}-id`;
                    input.value = '';
                });
                
                newRow.querySelectorAll('.search-box-id').forEach((input) => {
                    input.name = `ingredientperrecipe_set-${counter}-ingredient`;
                    input.id = `ingredientperrecipe_set-${counter}-ingredient`;
                    input.value = '';
                });

                newRow.querySelectorAll('.search-box').forEach((input) => {
                    input.value = '';
                });

                newRow.querySelectorAll('.amount-input').forEach((input) => {
                    input.name = `ingredientperrecipe_set-${counter}-amount`;
                    input.id = `ingredientperrecipe_set-${counter}-amount`;
                    input.value = '';
                });

                newRow.querySelectorAll('.unit-input').forEach((input) => {
                    input.name = `ingredientperrecipe_set-${counter}-unit`;
                    input.id = `ingredientperrecipe_set-${counter}-unit`;
                    input.value = '';
                });
                
                const formset = document.querySelector('#ingredient-formset tbody');
                formset.appendChild(newRow);

                counter++;

                let totalForms = document.querySelector('#id_ingredientperrecipe_set-TOTAL_FORMS');
                let currentCount = parseInt(totalForms.value);
            
                totalForms.value = currentCount + 1;

                const suggestions = document.createElement('ul');
                suggestions.id = 'suggestions';
                suggestions.className = 'list-group position-absolute suggestions';
                suggestions.style.width = '100%';

                

                const newSearchBox = newRow.querySelector('.search-box');
                const suggestionsContainer = newRow.querySelector('.suggestions');
                handleInput(newSearchBox, suggestionsContainer);
                
        
                const newButton = newRow.querySelector('.add-button');
                addRowEventListener(newButton);

                const deleteButton = newRow.querySelector('.remove-button');
                deleteButton.removeAttribute('disabled');
                
                deleteButton.addEventListener('click', function(event) {
                    event.preventDefault();
                    newRow.remove();
                    totalForms.value = totalForms.value - 1;
                });    
            });
        }

        const initialButton = document.getElementById('add-ingredient-button');
        addRowEventListener(initialButton);
    }
        

    // Recipe Steps
    const recipeSteps = document.querySelector('#steps-table')
    if (recipeSteps) {
            
        let initialStepForms = document.getElementById('id_step_set-INITIAL_FORMS').value;
        let stepCounter = parseInt(initialStepForms) + 1;

        
        function addStepEventListener(button) {
            button.addEventListener('click', function(event) {
                event.preventDefault();
                // console.log("add a step clicked");
                // console.log("counter = ", parseInt(stepCounter));
        
                const stepRow = document.getElementById('steprow');
                const newStepRow = stepRow.cloneNode(true);

                newStepRow.querySelectorAll('.step-id-input').forEach((input) => {
                    input.name = `step_set-${stepCounter}-id`;
                    input.id = `step_set-${stepCounter}-id`;
                });

                newStepRow.querySelectorAll('.input-group-text').forEach((span) => {
                    span.textContent = stepCounter + 1;
                });
                
                newStepRow.querySelectorAll('.step-number-input').forEach((input) => {
                    input.name = `step_set-${stepCounter}-step_number`;
                    input.id = `id_step_set-${stepCounter}-step_number`;
                    input.value = parseInt(input.value) + stepCounter;
                });

                newStepRow.querySelectorAll('.step-text-input').forEach((input) => {
                    input.name = `step_set-${stepCounter}-step_text`;
                    input.id = `id_step_set-${stepCounter}-step_text`;
                    input.value = '';
                });

                const newStepButton = newStepRow.querySelector('.add-step-0');
                newStepButton.className = `btn btn-outline-light add-step-${stepCounter}`;
            
                const stepFormset = document.querySelector('#steps-table tbody');
                stepFormset.appendChild(newStepRow);
                
                button.setAttribute('disabled', true);
                newStepButton.removeAttribute('disabled');
                
                let totalStepForms = document.querySelector('#id_step_set-TOTAL_FORMS');
                let currentCount = parseInt(totalStepForms.value);               

                const newDeleteStepButton = newStepRow.querySelector('.remove-step-0');
                newDeleteStepButton.className = `btn-close remove-step-${stepCounter} m-2`;
                document.querySelectorAll(`.btn-close.remove-step-${stepCounter - 1}.m-2`).forEach((btn) => {
                    btn.setAttribute('disabled', true);
                });
                newDeleteStepButton.removeAttribute('disabled');

                stepCounter++;
                totalStepForms.value = currentCount + 1;

                addStepEventListener(newStepButton);
                
                newDeleteStepButton.addEventListener('click', function(event) {
                    event.preventDefault();
                    // console.log("counter minus = ", stepCounter -2);

                    newStepRow.remove();

                    totalStepForms.value = totalStepForms.value - 1;
                    stepCounter --;
                    const lastStepButton = document.querySelector(`.add-step-${stepCounter - 1}`);
                    if (lastStepButton) {
                        lastStepButton.removeAttribute('disabled');
                    }
                    if (stepCounter > 1) {
                        const previousDeleteButton = document.querySelector(`.remove-step-${stepCounter - 1}`);
                        if (previousDeleteButton) {
                            previousDeleteButton.removeAttribute('disabled');
                        }
                    } 
                });    
            });
        }

        const initialStepButton = document.getElementById('add-step-button');
        addStepEventListener(initialStepButton);   
    }

    // Clear suggestions
    function clearContent(...elements) {
        elements.forEach(element => {
            // console.log("clearContent called");
            element.innerHTML = '';
            element.value = '';
        });
    }

    // Image Display and Upload
    
    imageUploader('imageUpload', 'modal', 'image', 'imagePreview', 'saveButton', 'cancelButton', 'closeButton'); // Add recipe cropper - bypass AJAX
    imageUploader('pictureUpload', 'picModal', 'picImage', 'picImagePreview', 'picSaveButton', 'picCancelButton', 'picCloseButton'); // Update profile pic

    document.querySelectorAll('.recipe-image-upload').forEach(input => {
        const recipeID = input.getAttribute('data-recipe-id');
        // console.log("for each:", recipeID)
        imageUploader(`imageUpload${recipeID}`, `modal${recipeID}`, `image${recipeID}`, `imagePreview${recipeID}`, `saveButton${recipeID}`, `cancelButton${recipeID}`, `closeButton${recipeID}`); // Update recipe image from recipe ID
    });
    

    function imageUploader(imageUploadId, modalId, imageId, imagePreviewId, saveButtonId, cancelButtonId, closeButtonId) {
        const imageUpload = document.getElementById(imageUploadId);
        const modalElement = document.getElementById(modalId);
        const image = document.getElementById(imageId);
        const preview  = document.getElementById(imagePreviewId);
        const saveButton = document.getElementById(saveButtonId);
        const cancelButton = document.getElementById(cancelButtonId);
        const closeButton = document.getElementById(closeButtonId);
        let cropper;

        if (imageUpload) {
        
            imageUpload.addEventListener('change', function (event) {
                const [file] = event.target.files;
        
                if (file) {
                    image.src = URL.createObjectURL(file);

                    const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);
                    modalInstance.show();
        
                    modalElement.addEventListener('shown.bs.modal', function () {
                        image.style.display = ''; 
                        if (cropper) {
                            cropper.destroy();
                        }
        
                        cropper = new Cropper(image, {
                            viewMode: 2,
                            aspectRatio: 1,
                            autoCropArea: 1,
                            responsive: true,
                        });
                    });
                    
                    saveButton.addEventListener('click', function(event) {
                        event.preventDefault();
                        
                        if (cropper) {
                            
                            // console.log("Save Clicked")
                            cropper.getCroppedCanvas({
                                width: 300,
                                height: 300,
                            }).toBlob((blob) => {
                                const url = URL.createObjectURL(blob);
                                preview.src = url;

                                const newFile = new File([blob], file.name, { type: "image/jpeg" });
                                const dataTransfer = new DataTransfer();
                                dataTransfer.items.add(newFile);
                                imageUpload.files = dataTransfer.files;

                                const formData = new FormData();
                                
                                let fetchURL = "";
                                const recipeID = imageUpload.getAttribute('data-recipe-id');

                                if (imageUploadId === "pictureUpload") {
                                    formData.append('croppedImage', newFile);
                                    fetchURL = '/user_dashboard/';
                                    uploadImage(formData, fetchURL);
                                    modalInstance.hide();

                                } else if (imageUploadId === `imageUpload${recipeID}`) {
                                    formData.append('croppedImage', newFile);
                                    formData.append('recipeID', recipeID);
                                    fetchURL = '/update_recipe_image/';
                                    uploadImage(formData, fetchURL);
                                    modalInstance.hide();
                                    
                                } else {
                                    modalInstance.hide();
                                }
                            }, "image/jpeg"); 
                        }
                        
                    });

                    cancelButton.addEventListener('click', function() {
                        imageUpload.value = '';
                        image.src = '';
                    });

                    closeButton.addEventListener('click', function() {
                        imageUpload.value = '';
                        image.src = '';
                    });
                    
                    modalElement.addEventListener('hidden.bs.modal', function () {
                        if (cropper) {
                            cropper.destroy();
                            cropper = null;
                        }
                        image.src = '';
                    });
                }
            });
        }
    }

    // Image Upload AJAX function
    function uploadImage(formData, fetchURL) {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        fetch(fetchURL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                // console.log('Upload success');
            } else {
                // console.log('Upload error');
            }
        })
    }


    // Rename Recipe
    const addRecipe = document.getElementById('addRecipe');
    if (addRecipe) {
        addRecipe.addEventListener('submit', function(event) {
            event.preventDefault();
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            const formData = new FormData(document.getElementById('addRecipe'));
            fetch('/add_recipe/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.rename) {
                    // console.log('Rename:', data.rename);
                    document.getElementById("renameModalBody").innerText = data.rename;
                    const renameModal = new bootstrap.Modal(document.getElementById("renameModal"));
                    renameModal.show();
                } else if (data.success) {
                    // console.log('Success. Recipe ID:', data.recipe_id);
                    window.location.href = `/recipe/${data.recipe_id}`;
                } else {
                    // console.log('Unexpected response:', data);
                }
            })
        });
    }

    // Confirm Delete
    const confirmDeleteButtons = document.querySelectorAll('.confirm-delete')
    if (confirmDeleteButtons) {
        confirmDeleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const formId = this.getAttribute('data-form-id');
                // console.log(formId)
                document.getElementById(formId).submit();
            });
        });
    }
});
    
    
// Favourite recipe function
function favRecipe(recipeId, event) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const likeButtonElement = event.currentTarget;
    const heartIcon = `
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-heart btn-custom-icon" viewBox="0 0 16 16">
            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
        </svg>
    `;

    const heartIconFilled = `
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-heart-fill btn-custom-icon" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
        </svg>
    `;

    fetch(`/favourite/${recipeId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ id: recipeId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.favourite) {
            likeButtonElement.innerHTML = heartIconFilled
            // console.log("Favourite")
        } else {
            likeButtonElement.innerHTML = heartIcon
            // console.log("Not favourite")
        }
    })
}

// Go back
const backButton = document.getElementById("backButton")
if (backButton) {

    backButton.addEventListener("click", function() { 
        history.back(); 
    });
}


// Show Password
function togglePassword() {
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmation");
    if (password.type === "password") {
        password.type = "text";
        if (confirmPassword) {
            confirmPassword.type = "text";
        }
    } else {
        password.type = "password";
        if (confirmPassword) {
            confirmPassword.type = "password";
        }
    }
}