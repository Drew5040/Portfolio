
// Helper function that checks for strings
function isAlpha(value) {
    return /^[a-zA-Z]+$/.test(value);
 }

// Helper function that checks for a '-'
function isDash(value) {
    return value === '-';
 }

// Function to add red border for invalid input
function addRedBorder(inputElement) {
    inputElement.classList.add('error-input');
 }

// Function to remove red border for invalid input
function removeRedBorder(inputElement) {
    inputElement.classList.remove('error-input');
 }

// Function to add or take away red stars depending on input
function toggleRedStar(show, id) {
    var redStar = document.getElementById(id);
    if (redStar) {
        if (show) {
            redStar.style.display = 'inline'; // Show the star
     } else {
            redStar.style.display = 'none'; // Hide the star
     }
   }
 }

// Validate the form by checking if all fields are filled in
function validateForm() {
    var form = document.getElementById('predictionForm');
    if (!form.checkValidity()) {
        alert('Please fill out all fields correctly');
        return false;
    }
    return true;
 }

// Function to hide the prediction box
function hidePrediction() {
    var predictionElement = document.getElementById('prediction');
    console.log(predictionElement);  // Check if the element is being correctly identified
    if (predictionElement) {
        predictionElement.style.display = 'none';
    }
 }

 // Existing logic to hide prediction when any form field is focused
    var inputFields = document.querySelectorAll('input, select');
    inputFields.forEach(function(field) {
        field.addEventListener('focus', function() {
            hidePrediction();
        });
    });

// Real-time validation for Age
function validateAge() {
    var ageInput = document.getElementById('age');
    var age = parseFloat(ageInput.value, 10);
    var isDecimal = ageInput.value.indexOf('.') !== -1;
    if (isAlpha(age) || age < 17 || age > 90 || isDecimal) {
        addRedBorder(ageInput);
        var show = true;
        toggleRedStar(show, 'star0');

    } else {
        removeRedBorder(ageInput);
        var show = false;
        toggleRedStar(show, 'star0');

    }
  }

// Real-time validation for Occupational Sector
function validateOs() {
    var osInput = document.getElementById('w_class');
    if (isDash(osInput.value)) {
        addRedBorder(osInput);
        var show = true;
        toggleRedStar(show, 'star1');
    } else {
        removeRedBorder(osInput);
        var show = false;
        toggleRedStar(show, 'star1');
    }
  }

// Real-time validation for Education
function validateEdu() {
    var eduInput = document.getElementById('edu');
    if (isDash(eduInput.value)) {
        addRedBorder(eduInput);
        var show = true;
        var id = 'star2';
        toggleRedStar(show, id);
    } else {
        removeRedBorder(eduInput);
        var show = false;
        var id = 'star2';
        toggleRedStar(show, id);
    }
  }

// Real-time validation for Marital Status
function validateMarStat() {
    var msInput = document.getElementById('marital_stat');
    if (isDash(msInput.value)) {
        addRedBorder(msInput);
        var show = true;
        toggleRedStar(show, 'star3');
    } else {
        removeRedBorder(msInput);
        var show = false;
        var id = 'star3';
        toggleRedStar(show, 'star3');
    }
  }

// Real-time validation for Occupation
function validateOcc() {
    var occInput = document.getElementById('occupation');
    if (isDash(occInput.value)) {
        addRedBorder(occInput);
        var show = true;
        var id = 'star4';
        toggleRedStar(show, id);
    } else {
        removeRedBorder(occInput);
        var show = false;
        var id = 'star4';
        toggleRedStar(show, id);
    }
  }

// Real-time validation for Relationship
function validateRel() {
    var relInput = document.getElementById('relation');
    if (isDash(relInput.value)) {
        addRedBorder(relInput);
        var show = true;
        var id = 'star5';
        toggleRedStar(show, id);
    } else {
        removeRedBorder(relInput);
        var show = false;
        var id = 'star5';
        toggleRedStar(show, id);
    }
  }

// Real-time validation for Race
function validateRace() {
    var raceInput = document.getElementById('race');
    if (isDash(raceInput.value)) {
        addRedBorder(raceInput);
        var show = true;
        var id = 'star6';
        toggleRedStar(show, id);
    } else {
        removeRedBorder(raceInput);
        var show = false;
        var id = 'star6';
        toggleRedStar(show, id);
    }
  }

// Real-time validation for Gender
function validateGender() {
    var genderInput = document.getElementById('gender');
    if (isDash(genderInput.value)) {
        addRedBorder(genderInput);
        var show = true;
        var id = 'star7';
        toggleRedStar(show, id);
    } else {
        removeRedBorder(genderInput);
        var show = false;
        var id = 'star7';
        toggleRedStar(show, id);
    }
  }

// Real-time validation for Capital Gain
function validateGain() {
    var gainInput = document.getElementById('c_gain');
    var gain = parseFloat(gainInput.value, 10);
    var isDecimal = gainInput.value.indexOf('.') !== -1;
    if (isAlpha(gain) || gain < 0 || gain > 99999 || isDecimal ) {
        addRedBorder(gainInput);
        var show = true;
        var id = 'star8';
        toggleRedStar(show, id);
    } else {
        removeRedBorder(gainInput);
        var show = false;
        var id = 'star8';
        toggleRedStar(show, id);
    }
  }

// Real-time validation for Capital Loss
function validateLoss() {
    var lossInput = document.getElementById('c_loss');
    var loss = parseFloat(lossInput.value, 10);
    var isDecimal = lossInput.value.indexOf('.') !== -1;
    if (isAlpha(loss) || loss < 0 || loss > 4356 || isDecimal ) {
        addRedBorder(lossInput);
        var show = true;
        var id = 'star9';
        toggleRedStar(show, id);
    } else {
        removeRedBorder(lossInput);
        var show = false;
        var id = 'star9';
        toggleRedStar(show, id);
    }
  }

// Real-time validation for Hours Per Week
function validateHours() {
    var hoursInput = document.getElementById('hours_per_week');
    var hours = parseFloat(hoursInput.value, 10);
    var isDecimal = hoursInput.value.indexOf('.') !== -1;
    if (isAlpha(hours) || hours < 1 || hours > 99 || isDecimal) {
        addRedBorder(hoursInput);
        var show = true;
        var id = 'star10';
        toggleRedStar(show, id);
    } else {
        removeRedBorder(hoursInput);
        var show = false;
        var id = 'star10';
        toggleRedStar(show, id);
    }
  }

// Real-time validation for Native Country
function validateNat() {
    var natInput = document.getElementById('native-country');
    if (isDash(natInput.value)) {
        addRedBorder(natInput);
        var show = true;
        var id = 'star11';
        toggleRedStar(show, id);
    } else {
        removeRedBorder(natInput);
        var show = false;
        var id = 'star11';
        toggleRedStar(show, id);
    }
  }

// Attach input event listeners for real-time validation
if (document.getElementById('age')) {
    document.getElementById('age').addEventListener('input', validateAge);
}

if (document.getElementById('w_class')) {
    document.getElementById('w_class').addEventListener('input', validateOs);
}
if (document.getElementById('edu')) {
    document.getElementById('edu').addEventListener('input', validateEdu);
}

if (document.getElementById('marital_stat')) {
    document.getElementById('marital_stat').addEventListener('input', validateMarStat);
}

if (document.getElementById('occupation')) {
    document.getElementById('occupation').addEventListener('input', validateOcc);
}

if (document.getElementById('relation')) {
    document.getElementById('relation').addEventListener('input', validateRel);
}

if (document.getElementById('race')) {
    document.getElementById('race').addEventListener('input', validateRace);
}

if (document.getElementById('gender')) {
    document.getElementById('gender').addEventListener('input', validateGender);
}

if (document.getElementById('c_gain')) {
    document.getElementById('c_gain').addEventListener('input', validateGain);
}

if (document.getElementById('c_loss')) {
    document.getElementById('c_loss').addEventListener('input', validateLoss);
}

if (document.getElementById('hours_per_week')) {
    document.getElementById('hours_per_week').addEventListener('input', validateHours);
}

if (document.getElementById('native-country')) {
    document.getElementById('native-country').addEventListener('input', validateNat);
}

// Function to run all validations at once
function validateAllFields() {
    validateAge();
    validateOs();
    validateEdu();
    validateMarStat();
    validateOcc();
    validateRel();
    validateRace();
    validateGender();
    validateGain();
    validateLoss();
    validateHours();
    validateNat();
}

// Function that reevaluates each field for correct entries when content is loaded or reloaded on the page
document.addEventListener('DOMContentLoaded', function() {
    validateAllFields();
});