<template>
    <form @submit.prevent="validateInput" class="mt-1 temperature-section">
        <!-- Temperature Section -->
        <div>
            <div class="form-group">
                <label for="ruleName">Rule Name</label>
                <input 
                    type="text" 
                    v-model="ruleName" 
                    id="ruleName" 
                    class="text-feild" 
                    placeholder="Enter Rule Name"
                    required
                />
            </div>

            <div class="form-group">
                <label for="condition">If Temperature is:</label>
                <select v-model="selectedCondition" id="condition" class="text-feild dropdown">
                    <option value=">" disabled>Select</option>
                    <option value=">">Greater than</option>
                    <option value="<">Less than</option>
                    <option value=">=">Greater than or equal</option>
                    <option value="<=">Less than or equal</option>
                    <option value="=">Equal to</option>
                </select>
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

const selectedCondition = ref('>'); // Default condition
const temperatureValue = ref(0); // Default temperature value
const ruleName = ref('');
const errorMessage = ref('');
const minTemperature = ref(-100); // Minimum temperature
const maxTemperature = ref(100); // Maximum temperature

const validateInput = () => {
    const temperature = parseFloat(temperatureValue.value);

    if (isNaN(temperature)) {
        errorMessage.value = "Please enter a valid number for temperature.";
    } else if (temperature < minTemperature.value || temperature > maxTemperature.value) {
        errorMessage.value = `Temperature must be between ${minTemperature.value}°C and ${maxTemperature.value}°C.`;
    } else {
        errorMessage.value = ""; // Clear error if input is valid
        alert(`Rule Name: ${ruleName.value}\nCondition: ${selectedCondition.value} ${temperatureValue.value}°C`);
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