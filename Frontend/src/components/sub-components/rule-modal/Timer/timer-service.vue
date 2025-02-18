<template>
    <form @submit.prevent="createRule" class="mt-1 temperature-section">
      <!-- Timer Section -->
      <div>
        <div class="form-group">
          <label for="ruleName">Trigger Name</label>
          <input
            type="text"
            v-model="ruleName"
            id="ruleName"
            class="text-feild"
            placeholder="Enter Trigger Name"
            required
          />
        </div>
        <div class="form-group">
          <label for="condition">Select Timer:</label>
          <select v-model="selectedCondition" id="condition" class="text-feild dropdown">
            <option value="" disabled selected>Select</option>
            <option value="Every Minute">Every Minute</option>
            <option value="Every Hour">Every Hour</option>
            <option value="Every Day">Every Day</option>
            <option value="Every Week">Every Week</option>
            <option value="Every Month">Every Month</option>
            <option value="Every Year">Every Year</option>
          </select>
        </div>
        <button type="submit" class="button-2 mt-4">Create</button>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    </form>
  </template>

<script setup>
import { ref } from 'vue';
import axios from 'axios'; // Import Axios for making HTTP requests

// Reactive variables
const ruleName = ref(''); // Trigger name
const selectedCondition = ref(''); // Selected timer condition
const errorMessage = ref(''); // Error message for validation

// Function to create a new rule via POST request
const createRule = async () => {
  errorMessage.value = ''; // Reset error message

  // Validation
  if (!ruleName.value.trim()) {
    errorMessage.value = "Please enter a valid Trigger name.";
    return;
  }
  if (!selectedCondition.value) {
    errorMessage.value = "Please select a timer.";
    return;
  }

  try {
    // Prepare the payload for the POST request
    const payload = {
      service_id: 2, // Service ID for Timer
      name: ruleName.value,
      condition: selectedCondition.value // Timer condition
    };

    // Log the payload for debugging
    console.log("Payload:", payload);

    // Send the POST request to the API endpoint
    const response = await axios.post('http://127.0.0.1:5000/rules', payload);

    // Handle successful response
    console.log("Server Response:", response.data);
    alert("Rule created successfully!");
    resetForm(); // Reset the form after successful creation
    location.reload();
  } catch (error) {
    // Handle errors
    if (error.response) {
      errorMessage.value = `Error creating rule: ${error.response.data.message || error.response.statusText}`;
      console.error("Server Response:", error.response.data); // Log the full response
    } else {
      errorMessage.value = "An unexpected error occurred. Please try again later.";
    }
    console.error("Error creating rule:", error);
  }
};

// Function to reset the form
const resetForm = () => {
  ruleName.value = '';
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