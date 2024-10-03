
document.getElementById('add-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    fetch('/api/add', {
        method: 'POST',
        body: data
    }).then(response => response.json()).then(data => {
        console.log('Data added:', data);
    }).catch(error => console.error('Error adding data:', error));
});

document.getElementById('edit-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    fetch('/api/edit', {
        method: 'POST',
        body: data
    }).then(response => response.json()).then(data => {
        console.log('Data edited:', data);
    }).catch(error => console.error('Error editing data:', error));
});

document.getElementById('remove-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    fetch('/api/remove', {
        method: 'POST',
        body: data
    }).then(response => response.json()).then(data => {
        console.log('Data removed:', data);
    }).catch(error => console.error('Error removing data:', error));
});
