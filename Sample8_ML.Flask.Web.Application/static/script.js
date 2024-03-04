
function isAlpha(value) {
    return /^[a-zA-Z]+$/.test(value);
}

function isDash(value) {
    return value === '-';
}

// Function to add red border for invalid input
function addRedBorder(inputElement) {
    inputElement.classList.add('error-input');
}

function removeRedBorder(inputElement) {
    inputElement.classList.remove('error-input')
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
    } else {
        removeRedBorder(ageInput);
     }
 }

// Real-time validation for Occupational Sector
function validateOs() {
    var osInput = document.getElementById('w_class');
    if (isDash(osInput.value)) {
        addRedBorder(osInput);
    } else {
        removeRedBorder(osInput);
    }
  }

// Real-time validation for Education
function validateEdu() {
    var eduInput = document.getElementById('edu');
    if (isDash(eduInput.value)) {
        addRedBorder(eduInput);
    } else {
        removeRedBorder(eduInput);
    }
  }

// Real-time validation for Marital Status
function validateMarStat() {
    var msInput = document.getElementById('marital_stat');
    if (isDash(msInput.value)) {
        addRedBorder(msInput);
    } else {
        removeRedBorder(msInput);
    }
  }

// Real-time validation for Occupation
function validateOcc() {
    var occInput = document.getElementById('occupation');
    if (isDash(occInput.value)) {
        addRedBorder(occInput);
    } else {
        removeRedBorder(occInput);
    }
  }

// Real-time validation for Relationship
function validateRel() {
    var relInput = document.getElementById('relation');
    if (isDash(relInput.value)) {
        addRedBorder(relInput);
    } else {
        removeRedBorder(relInput);
    }
  }

// Real-time validation for Race
function validateRace() {
    var raceInput = document.getElementById('race');
    if (isDash(raceInput.value)) {
        addRedBorder(raceInput);
    } else {
        removeRedBorder(raceInput);
    }
  }

// Real-time validation for Gender
function validateGender() {
    var genderInput = document.getElementById('gender');
    if (isDash(genderInput.value)) {
        addRedBorder(genderInput);
    } else {
        removeRedBorder(genderInput);
    }
  }

// Real-time validation for Capital Gain
function validateGain() {
    var gainInput = document.getElementById('c_gain');
    var gain = parseFloat(gainInput.value, 10);
    var isDecimal = gainInput.value.indexOf('.') !== -1;
    if (isAlpha(gain) || gain < 0 || gain > 99999 || isDecimal ) {
        addRedBorder(gainInput);
    } else {
        removeRedBorder(gainInput);
    }
  }

// Real-time validation for Capital Loss
function validateLoss() {
    var lossInput = document.getElementById('c_loss');
    var loss = parseFloat(lossInput.value, 10);
    var isDecimal = lossInput.value.indexOf('.') !== -1;
    if (isAlpha(loss) || loss < 0 || loss > 4356 || isDecimal ) {
        addRedBorder(lossInput);
    } else {
        removeRedBorder(lossInput);
    }
  }

// Real-time validation for Hours Per Week
function validateHours() {
    var hoursInput = document.getElementById('hours_per_week');
    var hours = parseFloat(hoursInput.value, 10);
    var isDecimal = hoursInput.value.indexOf('.') !== -1;
    if (isAlpha(hours) || hours < 1 || hours > 99 || isDecimal) {
        addRedBorder(hoursInput);
    } else {
        removeRedBorder(hoursInput);
    }
}

// Real-time validation for Native Country
function validateNat() {
    var natInput = document.getElementById('native-country');
    if (isDash(natInput.value)) {
        addRedBorder(natInput);
    } else {
        removeRedBorder(natInput);
    }
  }

// Attach input event listeners for real-time validation
document.getElementById('age').addEventListener('input', validateAge);
document.getElementById('w_class').addEventListener('input', validateOs);
document.getElementById('edu').addEventListener('input', validateEdu);
document.getElementById('marital_stat').addEventListener('input', validateMarStat);
document.getElementById('occupation').addEventListener('input', validateOcc);
document.getElementById('relation').addEventListener('input', validateRel);
document.getElementById('race').addEventListener('input', validateRace);
document.getElementById('gender').addEventListener('input', validateGender);
document.getElementById('c_gain').addEventListener('input', validateGain);
document.getElementById('c_loss').addEventListener('input', validateLoss);
document.getElementById('hours_per_week').addEventListener('input', validateHours);
document.getElementById('native-country').addEventListener('input', validateNat);

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








