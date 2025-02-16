<template>
    <form @submit.prevent="createRule" class="mt-1 temperature-section">
      <!-- Temperature Section -->
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
          <label for="condition">If Temperature is:</label>
          <select v-model="selectedCondition" id="condition" class="text-feild dropdown">
            <option value="" disabled selected>Select</option>
            <option value=">">Greater than</option>
            <option value="<">Less than</option>
            <option value=">=">Greater than or equal</option>
            <option value="<=">Less than or equal</option>
            <option value="=">Equal to</option>
          </select>
        </div>
        <div class="form-group">
          <label for="temperatureValue">Select Temperature:</label>
          <div class="slider-container">
            <input
              type="range"
              v-model="temperatureValue"
              id="temperatureValue"
              class="slider"
              :min="minTemperature"
              :max="maxTemperature"
              step="0.1"
              :class="{'input-error': errorMessage}"
            />
            <span class="slider-value">{{ temperatureValue }}°C</span>
          </div>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        </div>
        <button type="submit" class="button-2 mt-4">Create</button>
      </div>
    </form>
  </template>

<script setup>
import { ref } from 'vue';
import axios from 'axios'; // Import Axios for making HTTP requests

// Reactive variables
const ruleName = ref(''); // Trigger name
const selectedCondition = ref(''); // Selected condition (e.g., ">", "<", etc.)
const temperatureValue = ref(0); // Selected temperature value
const errorMessage = ref(''); // Error message for validation
const minTemperature = ref(-100); // Minimum temperature
const maxTemperature = ref(100); // Maximum temperature

// Function to validate input and create a new rule via POST request
const createRule = async () => {
  errorMessage.value = ''; // Reset error message

  // Validation
  if (!ruleName.value.trim()) {
    errorMessage.value = "Please enter a valid Rule name.";
    return;
  }
  if (!selectedCondition.value) {
    errorMessage.value = "Please select a condition.";
    return;
  }
  const temperature = parseFloat(temperatureValue.value);
  if (isNaN(temperature)) {
    errorMessage.value = "Please enter a valid number for temperature.";
    return;
  }
  if (temperature < minTemperature.value || temperature > maxTemperature.value) {
    errorMessage.value = `Temperature must be between ${minTemperature.value}°C and ${maxTemperature.value}°C.`;
    return;
  }

  try {
    // Prepare the payload for the POST request
    const payload = {
      service_id: 1, // Service ID for Temperature
      name: ruleName.value,
      condition: `${selectedCondition.value} ${temperatureValue.value}`, // Combine condition and temperature
      range_value: temperatureValue.value // Include the range value
    };

    // Log the payload for debugging
    console.log("Payload:", payload);

    // Send the POST request to the API endpoint
    const response = await axios.post('http://127.0.0.1:5000/rules', payload);

    // Handle successful response
    console.log("Server Response:", response.data);
    alert("Rule created successfully!");
    resetForm(); // Reset the form after successful creation
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
  temperatureValue.value = 0;
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