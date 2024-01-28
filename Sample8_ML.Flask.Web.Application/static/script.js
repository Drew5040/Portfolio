	function validateForm() {
		var form = document.querySelector('predictionForm');
		if (!form.checkValidity()) {
			alert('Please fill out all fields correctly');
			return false;
		}
		return true;
	}