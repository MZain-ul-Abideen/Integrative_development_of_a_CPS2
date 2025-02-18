<template>
    <form @submit.prevent="createRule" class="mt-1 temperature-section">
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
          <label for="condition">If Weather is:</label>
          <select v-model="selectedCondition" id="condition" class="text-feild dropdown">
            <option value="" disabled selected>Select</option>
            <option value="Rainy">Rainy</option>
            <option value="Cloudy">Cloudy</option>
            <option value="Sunny">Sunny</option>
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
  const ruleName = ref(''); // Trigger name
  const selectedCondition = ref(''); // Selected weather condition
  const errorMessage = ref(''); // Error message for validation
  
  // Function to validate input and create a new rule via POST request
  const createRule = async () => {
    errorMessage.value = ''; // Reset error message
  
    // Validation
    if (!ruleName.value.trim()) {
      errorMessage.value = "Please enter a valid Rule name.";
      return;
    }
    if (!selectedCondition.value) {
      errorMessage.value = "Please select a weather condition.";
      return;
    }
  
    try {
      // Prepare the payload for the POST request
      const payload = {
        service_id: 1, // Service ID for Weather
        name: ruleName.value,
        condition: selectedCondition.value // Weather condition (e.g., "Rainy", "Cloudy", "Sunny")
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
</style>