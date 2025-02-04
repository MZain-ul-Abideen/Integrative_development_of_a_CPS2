<template>
    <form @submit.prevent="validateInput" class="mt-1 temperature-section">
        <!-- Temperature Section -->
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
                <label for="temperatureValue">Set Temperature:</label>
                <div class="slider-container">
                    <input 
                        type="range" 
                        v-model="temperatureValue" 
                        id="temperatureValue" 
                        class="slider" 
                        :min="minTemperature"
                        :max="maxTemperature"
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

// Refs
const actionName = ref(''); // Stores the action name
const temperatureValue = ref(0); // Default temperature value
const errorMessage = ref(''); // Stores error messages
const minTemperature = ref(-100); // Minimum temperature
const maxTemperature = ref(100); // Maximum temperature

// Validate input
const validateInput = () => {
    const temperature = parseFloat(temperatureValue.value);

    if (isNaN(temperature)) {
        errorMessage.value = "Please enter a valid number for temperature.";
    } else if (temperature < minTemperature.value || temperature > maxTemperature.value) {
        errorMessage.value = `Temperature must be between ${minTemperature.value}°C and ${maxTemperature.value}°C.`;
    } else {
        errorMessage.value = ""; // Clear error if input is valid
        alert(`Action Name: ${actionName.value}\nTemperature: ${temperatureValue.value}°C`);
    }
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