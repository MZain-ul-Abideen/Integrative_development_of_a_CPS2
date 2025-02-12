<template>
    <form @submit.prevent="validateInput" class="mt-1 temperature-section">
        <!-- Temperature Section -->
        <div>
            <div class="form-group">
                <label for="ruleName">Rule Name</label>
                <input type="text" v-model="ruleName" id="ruleName" class="text-feild" placeholder="Enter Rule Name"
                    required />
            </div>

            <div class="form-group">
                <label for="condition">Select Timer:</label>
                <select v-model="selectedCondition" id="condition" class="text-feild dropdown">
                    <option value=">" disabled>Select</option>
                    <option value=">">Every Minute</option>
                    <option value="<">Every Hour</option>
                    <option value=">=">Every Day</option>
                    <option value="<=">Every Week</option>
                    <option value="=">Every Month</option>
                    <option value="=">Every Year</option>
                </select>
            </div>

            <!-- Select to Send (Checkboxes) -->
            <!-- <div class="form-group mt-4">
                <label>Select to Send:</label>
                <div class="checkbox-group mt-2">
                    <label>
                        <input type="checkbox" v-model="selectedOptions" value="Weather Outside" /> Weather Outside
                    </label>
                    <label class="mx-4">
                        <input type="checkbox" v-model="selectedOptions" value="Temperature Inside" /> Temperature Inside
                    </label>
                </div>
            </div> -->

            <button type="submit" class="button-2 mt-4">Create</button>

            <div v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </div>
        </div>
    </form>
</template>

<script setup>
import { ref } from 'vue';

// Reactive variables
const ruleName = ref('');
const selectedTimer = ref('');
const selectedOptions = ref([]); // Array to store selected checkboxes
const errorMessage = ref('');
const selectedCondition = ref('>'); // Default condition

// Validation function
const validateInput = () => {
    errorMessage.value = ''; // Reset error message

    // Validate Rule Name
    if (!ruleName.value.trim()) {
        errorMessage.value = "Please enter a valid rule name.";
        return;
    }

    // Validate Timer Selection
    if (!selectedTimer.value) {
        errorMessage.value = "Please select a timer.";
        return;
    }

    // Validate Checkbox Selection
    if (selectedOptions.value.length === 0) {
        errorMessage.value = "Please select at least one option to send.";
        return;
    }

    // If all validations pass
    alert(`Rule Name: ${ruleName.value}\nTimer: ${selectedTimer.value}\nSelected Options: ${selectedOptions.value.join(', ')}`);
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