// Function to fetch facilities from the API
function fetchCategory(category) {
    const facilitiesDiv = document.getElementById('facilities');
    const categoryTitle = document.getElementById('category-title');

    // Update the category title
    categoryTitle.textContent = `Showing ${category}`;

    // Clear the facilities section
    facilitiesDiv.innerHTML = '';

    // Fetch data from backend API
    fetch(`http://localhost:8000/${category}`)
        .then(response => response.json())
        .then(data => {
            // Loop through each facility and display it
            data.forEach(facility => {
                const facilityCard = document.createElement('div');
                facilityCard.classList.add('facility-card');

                facilityCard.innerHTML = `
                    <h3>${facility.name}</h3>
                    <p>Location: ${facility.location}</p>
                    <p>Contact: ${facility.contact}</p>
                    <p>Hours: ${facility.hours}</p>
                `;

                facilitiesDiv.appendChild(facilityCard);
            });
        })
        .catch(error => {
            facilitiesDiv.innerHTML = `<p>Sorry, we couldn't load the data. Please try again later.</p>`;
            console.error('Error fetching data:', error);
        });
}
