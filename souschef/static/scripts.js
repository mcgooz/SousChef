document.addEventListener("DOMContentLoaded", function() {

    // Search via API and autocomplete
    const searchBox = document.getElementById('searchBox');
    const suggestionsContainer = document.getElementById('suggestions');
    
    if (searchBox && suggestionsContainer) {
        let suggestions = [];
        let debounceTimer; // Prevent API calls after each keystroke


        // Detect input in search box
        searchBox.addEventListener('input', function() {
            const query = this.value;
            this.value = this.value.replace(/[0-9]/g, '');

            if (query.length >= 2) {
                clearTimeout(debounceTimer); // Clear timer then restart at 500ms

                debounceTimer = setTimeout(function() {
                    fetchSuggestions(query);
                    searchBox.classList.add('autocomplete-active');
                }, 500);
                
            } else {
                clearTimeout(debounceTimer);
                clearContent(suggestionsContainer);
                searchBox.classList.remove('autocomplete-active');
                console.log('Clearing suggestions');
            }
        });

        // Fetch suggestions
        function fetchSuggestions(query) {
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
                
                displaySuggestions(details);
                console.log(details)
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
            });
        }

        // Display suggestions
        function displaySuggestions(details) {
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
                        
                        console.log(itemId)
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
                        .then(response => response.json())
                        .then(data => {
                            const itemAisle = data.aisle;
                            console.log(itemAisle);

                        // Item selection
                            if (!itemName) {
                                alert("Please select an item from the list");

                            } else {
                                console.log(itemName, itemId);
                                searchBox.value = itemName;
                                const itemInput = document.getElementById('ingredientId')
                                // const catInput = document.getElementById('itemCategory')
                                
                                itemInput.value = itemId;
                                clearContent(suggestionsContainer);
                            }
                        })
                    })
                })
            }
        }
    

        // Update recipe ingredeints
        const recipeIngredientInput = document.querySelector('#recipe_ingredient_input');
        if (recipeIngredientInput) {

            recipeIngredientInput.addEventListener('submit', function(event) {
                event.preventDefault();
                
                const formData = new FormData(this);

                fetch('/recipe_ingredient/', {
                    method: 'POST',
                    body: formData
                })

                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    const tableBody = document.querySelector('tbody');
                    const newRow = document.createElement('tr');

                    newRow.innerHTML = `
                    <td>${data.ingredient}</td>
                    <td>${data.amount}</td>
                    <td>${data.unit}</td>`;

                    tableBody.appendChild(newRow);
                    clearContent(searchBox, quantity, unit);
                })
                .catch(error => console.error('Error:', error));
            });
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
