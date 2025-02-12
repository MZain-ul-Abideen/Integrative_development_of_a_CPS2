<template>
    <form @submit.prevent="validateInput" class="mt-1 temperature-section">
        <!-- Email Action Section -->
        <div>
            <div class="form-group">
                <label for="ActionName">Action Name</label>
                <input type="text" v-model="ruleName" id="ActionName" class="text-feild" placeholder="Enter Action Name"
                    required />
            </div>

            <div class="form-group d-flex justify-content-center">
                <div class="d-flex align-items-center justify-content-between">
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider1"></span>
                    </label><label class="switch">
                        <input type="checkbox">
                        <span class="slider2"></span>
                    </label><label class="switch">
                        <input type="checkbox">
                        <span class="slider3"></span>
                    </label>
                </div>
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

/* From Uiverse.io by gharsh11032000 */
/* The switch - the box around the slider */
.switch {
    font-size: 17px;
    position: relative;
    display: inline-block;
    width: 3.5em;
    height: 2em;
    margin: 1rem;
}

/* Hide default HTML checkbox */
.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

/* The slider */
.slider1 {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background: #fbacac;
    border-radius: 50px;
    transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
}

.slider1:before {
    position: absolute;
    content: "";
    height: 1.4em;
    width: 1.4em;
    left: 0.3em;
    bottom: 0.3em;
    background-color: white;
    border-radius: 50px;
    box-shadow: 0 0px 20px rgba(0, 0, 0, 0.4);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.switch input:checked+.slider1 {
    background: #ce4f4f;
}

.switch input:focus+.slider1 {
    box-shadow: 0 0 1px #ce4f4f;
}

.switch input:checked+.slider1:before {
    transform: translateX(1.6em);
    width: 2em;
    height: 2em;
    bottom: 0;
}



/* The slider */
.slider2 {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background: #acfbb0;
    border-radius: 50px;
    transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
}

.slider2:before {
    position: absolute;
    content: "";
    height: 1.4em;
    width: 1.4em;
    left: 0.3em;
    bottom: 0.3em;
    background-color: white;
    border-radius: 50px;
    box-shadow: 0 0px 20px rgba(0, 0, 0, 0.4);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.switch input:checked+.slider2 {
    background: #4fce6f;
}

.switch input:focus+.slider2 {
    box-shadow: 0 0 1px #4fce6f;
}

.switch input:checked+.slider2:before {
    transform: translateX(1.6em);
    width: 2em;
    height: 2em;
    bottom: 0;
}



/* The slider */
.slider3 {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background: #acbefb;
    border-radius: 50px;
    transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
}

.slider3:before {
    position: absolute;
    content: "";
    height: 1.4em;
    width: 1.4em;
    left: 0.3em;
    bottom: 0.3em;
    background-color: white;
    border-radius: 50px;
    box-shadow: 0 0px 20px rgba(0, 0, 0, 0.4);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.switch input:checked+.slider3 {
    background: #574fce;
}

.switch input:focus+.slider3 {
    box-shadow: 0 0 1px #574fce;
}

.switch input:checked+.slider3:before {
    transform: translateX(1.6em);
    width: 2em;
    height: 2em;
    bottom: 0;
}
</style>