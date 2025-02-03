<template>
    <form @submit.prevent="validateInput" class="mt-1 temperature-section">
        <div>

            <div class="form-group">
                <label for="ruleName">Rule Name</label>
                <input type="text" v-model="ruleName" id="ruleName" class="text-feild" placeholder="Enter Rule Name"
                    required />
            </div>

            <div class="form-group">
                <label for="condition">If Weather is:</label>
                <select v-model="selectedCondition" id="condition" class="text-feild dropdown">
                    <option value="Select" disabled>Select</option>
                    <option value=">">Rainy</option>
                    <option value="<">Cloudy</option>
                    <option value=">=">Sunny</option>
                </select>
            </div>
            <button type="submit" class="button-2 mt-4">Create</button>
        </div>
    </form>
</template>

<script setup>
import { ref } from 'vue';

const selectedCondition = ref('Select'); // Default condition

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