document.addEventListener("DOMContentLoaded", function() {

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
                    console.log('Clearing suggestions');
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
                console.log(details)
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
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
                            console.log('Item ID', itemId)
                            console.log('Ingredient ID:', ingredientId);

                            if (!itemName) {
                                alert("Please select an item from the list");

                            } else {
                                
                                searchBox.value = itemName;

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
    

        // Update recipe ingredeints
        const recipeIngredientInput = document.querySelector('#ingredient-formset');
        if (recipeIngredientInput) {
            
            let counter = 1;
            function addRowEventListener(button) {
                button.addEventListener('click', function(event) {
                    event.preventDefault();
                    console.log("clicked");
            
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
                    deleteButton.style.display = 'inline-block';
                    
                    deleteButton.addEventListener('click', function(event) {
                        event.preventDefault();
                        newRow.remove();
                        totalForms.value = totalForms.value - 1;
                    });    
                });
            }

            const initialButton = document.getElementById('add-ingredient-button');
            addRowEventListener(initialButton);

            // const initialDeleteButton = document.querySelector('remove-ingredient-button');
            // initialDeleteButton.addEventListener('click', function(event) {
            //     event.preventDefault();
            //     initialDeleteButton.closest('tr').remove();
            // });
        }
        
    }
    
    // Clear suggestions
    function clearContent(...elements) {
        elements.forEach(element => {
            console.log("clearContent called");
            element.innerHTML = '';
            element.value = '';
        });
    }
});



// Show Password
function togglePassword() {
    var passwordField = document.getElementById("password");
    var confirmPasswordField = document.getElementById("confirmation");
    if (passwordField.type === "password") {
        passwordField.type = "text";
        confirmPasswordField.type = "text";
    } else {
        passwordField.type = "password";
        confirmPasswordField.type = "password";
    }
}



    // // Error messages
    // let alertMessage = document.getElementById('alert-message');
    // let form = document.querySelector('#pantryIngredientForm');
    // form.addEventListener('submit', function(event) {
    //     event.preventDefault();

    //     fetch('pantry', {
    //         method: 'POST',
    //         body: new FormData(pantryIngredientForm)
    //     })
    
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data);
    //         if (data.error) {
    //         alertMessage.innerHTML = `<div class="alert custom-alert alert-light alert-dismissible fade show" role="alert">
    //         ${data.error}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`;
    //         } else {
    //             window.location.reload();
    //         }
    //     });
    // });

    // const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

// Update List
// function updateList(event) {
//     event.preventDefault();
//     console.log("post stopped")
//     const ingredientToAdd = document.getElementById('searchBox');
//     const quantityToAdd = document.getElementById('quantity');
//     const unitToAdd = document.getElementById('unit');
//     const unitType = unitToAdd.selectedOptions[0].text;
//     const unitID = unitToAdd.value;

//     addIngredientToList(ingredientToAdd.value, quantityToAdd.value, unitType, unitID);

//     function clearSearch() {
//         ingredientToAdd.value = '';
//         quantityToAdd.value = '';
//         unitToAdd.value = '';
//     }

//     clearSearch();
// }

// // Add ingredient to list
// function addIngredientToList(ingredient, quantity, unitType, unitID) {
//     const ingredientList = document.getElementById("ingredientList");
//     const newIngredient = `${ingredient}`;
//     const newQuantity = Number(quantity);
//     const newUnit = `${unitType}`;

//     let exists = false;

//     // Check for existing ingredient
//     for (let i = 1; i < ingredientList.rows.length; i++) {
//         if (ingredientList.rows[i].cells[0].innerText === newIngredient) {
//             exists = true;

//             const ingredientData = {
//                 name: ingredientList.rows[i].cells[0].innerText,
//                 quantity: ingredientList.rows[i].cells[1].innerText,
//                 unit: {
//                     id: ingredientList.rows[i].cells[2].querySelector('input[name="unitID"]').value,
//                     unit_type: ingredientList.rows[i].cells[2].innerText, 
//                 }     
//             };

//             const unitData = {
//                 id: unitID,
//                 unit_type: unitType   
//             };
            
//             console.log(unitType)

//             async function updateMeasurement(ingredientData, newQuantity, unitData) {
//                 const response = await fetch('/table_update/', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json'
//                     },
//                     body: JSON.stringify({ingredientData, newQuantity, unitData})
//                 });

//                 const data = await response.json();
//                 if (data.status === 'success') {
//                     console.log(data);
//                     ingredientList.rows[i].cells[1].innerText = data.quantity;
//                     ingredientList.rows[i].cells[2].innerText = data.unit;
//                     ingredientList.rows[i].cells[2].hidden = data.unit_id;
//                 }
//             }
            
//             updateMeasurement(ingredientData, newQuantity, unitData);
//             console.log("updateMeasure called")
//         }      
//     }

//     if (!exists) {
//         // Define table elements
//         const row = ingredientList.insertRow();
//         const cell1 = row.insertCell(0);
//         const cell2 = row.insertCell(1);
//         const cell3 = row.insertCell(2);
//         const hidden = document.createElement("input");
//         hidden.type = "hidden";
//         hidden.name = "unitID";
//         hidden.value = unitID;
        
//         cell1.innerHTML = newIngredient;
//         cell2.innerHTML = newQuantity; 
//         cell3.innerHTML = newUnit;
//         cell3.appendChild(hidden);
//     }
    
//     ingredientList.style.display = "block";
// }

// const ingredient = document.getElementById('ingredientID');
//                 const ingredientId = document.getElementById('ingredientID');
//                 const amount = document.getElementById('amount');
//                 const unit = document.getElementById('unit');
