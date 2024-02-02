function validateForm() {
    var form = document.getElementById('predictionForm');
    if (!form.checkValidity()) {
        alert('Please fill out all fields correctly');
        return false;
    }
    return true;
}

function hidePrediction() {
    var predictionElement = document.getElementById('prediction');
    setTimeout(function() {
        predictionElement.style.display = 'none';
        console.log('Hiding prediction after 5 seconds...');
    }, 5000);
}

function onSubmitActions() {
    // Validate the form
    var isValid = validateForm();

    // If form is valid, hide the prediction after 5 seconds
    if (isValid) {
        setTimeout(hidePrediction, 0); // Call hidePrediction asynchronously
    }

    // Return the validation result
    return isValid;
}