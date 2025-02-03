<template>
    <form @submit.prevent="validateInput" class="mt-1 temperature-section">
        <!-- Email Action Section -->
        <div>
            <div class="form-group">
                <label for="ActionName">Action Name</label>
                <input 
                    type="text" 
                    v-model="ruleName" 
                    id="ActionName" 
                    class="text-feild" 
                    placeholder="Enter Action Name"
                    required
                />
            </div>

            <div class="form-group">
                <label for="EmailAddress">Email Address</label>
                <input 
                    type="email" 
                    v-model="emailAddress" 
                    id="EmailAddress" 
                    class="text-feild" 
                    placeholder="Enter Email Address"
                    required
                />
            </div>

            <button type="submit" class="button-2 mt-4">Create</button>
        </div>
    </form>
</template>

<script setup>
import { ref } from 'vue';

const ruleName = ref(''); // Stores the action name
const emailAddress = ref(''); // Stores the email address

const validateInput = () => {
    if (!ruleName.value || !emailAddress.value) {
        alert("Please fill out all fields.");
        return;
    }

    // If validation passes, show the entered data
    alert(`Action Name: ${ruleName.value}\nEmail Address: ${emailAddress.value}`);
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