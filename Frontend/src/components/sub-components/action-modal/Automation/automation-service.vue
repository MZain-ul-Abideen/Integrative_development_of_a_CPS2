<template>
    <form @submit.prevent="createAction" class="mt-1 temperature-section">
      <!-- Action Section -->
      <div>
        <div class="form-group">
          <label for="ActionName">Action Name</label>
          <input
            type="text"
            v-model="actionName"
            id="ActionName"
            class="text-feild"
            placeholder="Enter Action Name"
            required
          />
        </div>
        <div class="form-group">
          <label for="comfortLevel">Comfort Level:</label>
          <select v-model="selectedCondition" id="comfortLevel" class="text-feild dropdown">
            <option value="" disabled selected>Select</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
          </select>
        </div>
        <button type="submit" class="button-2 mt-4">Create</button>
      </div>
    </form>
  </template>

<script setup>
import { ref } from 'vue';
import axios from 'axios'; // Import Axios for making HTTP requests

// Reactive variables
const actionName = ref(''); // Action name
const selectedCondition = ref(''); // Selected comfort level
const errorMessage = ref(''); // Error message for validation

// Function to validate input and create a new action via POST request
const createAction = async () => {
  errorMessage.value = ''; // Reset error message

  // Validation
  if (!actionName.value.trim()) {
    errorMessage.value = "Please enter a valid Action name.";
    return;
  }
  if (!selectedCondition.value) {
    errorMessage.value = "Please select a Comfort Level.";
    return;
  }

  try {
    // Prepare the payload for the POST request
    const payload = {
      service_id: 4, // Service ID for Building Automation
      name: actionName.value,
      action_type: "Building Automation", // Action type
      parameters: {
        comfort_level: parseInt(selectedCondition.value, 10) // Convert comfort level to integer
      }
    };

    // Log the payload for debugging
    console.log("Payload:", payload);

    // Send the POST request to the API endpoint
    const response = await axios.post('http://127.0.0.1:5000/actions', payload);

    // Handle successful response
    console.log("Server Response:", response.data);
    alert("Action created successfully!");
    resetForm(); // Reset the form after successful creation
  } catch (error) {
    // Handle errors
    if (error.response) {
      errorMessage.value = `Error creating action: ${error.response.data.message || error.response.statusText}`;
      console.error("Server Response:", error.response.data); // Log the full response
    } else {
      errorMessage.value = "An unexpected error occurred. Please try again later.";
    }
    console.error("Error creating action:", error);
  }
};

// Function to reset the form
const resetForm = () => {
  actionName.value = '';
  selectedCondition.value = '';
};
</script>

<style scoped>
.temperature-section {
    width: 80%;
}

.form-group {
    text-align: left;
    margin-top: 1rem;
}

.temperature-section label {
    font-size: 1rem;
}


.slider-container {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.slider {
    width: 100%;
}

.slider-value {
    font-size: 1rem;
    font-weight: bold;
}

.error-message {
    color: var(--color-error);
    font-size: 0.875rem;
    margin-top: 0.25rem;
}

.input-error {
    border-color: var(--color-error);
}
</style>