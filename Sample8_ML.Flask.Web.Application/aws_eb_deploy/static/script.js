
// Validate the form by checking if all fields are filled in
function validateForm() {
    var form = document.getElementById('predictionForm');
    if (!form.checkValidity()) {
        alert('Please fill out all fields correctly');
        return false;
    }
    return true;
}

// Hide prediction function to remove old output from the screen when clicking in 'Age' field
function hidePrediction() {
    var predictionElement = document.getElementById('prediction');
    predictionElement.style.display = 'none';
}

// Add an event listener to the age input field
document.getElementById('age').addEventListener('focus', function () {
    hidePrediction();
});

