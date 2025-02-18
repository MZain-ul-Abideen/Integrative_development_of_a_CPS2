<template>
  <form @submit.prevent="createAction" class="mt-1 temperature-section">
    <!-- Email Action Section -->
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
        <label for="EmailAddress">Email Address</label>
        <input
          type="email"
          v-model="parameters.emailAddress"
          id="EmailAddress"
          class="text-feild"
          placeholder="Enter Email Address"
          required
        />
      </div>
      <div class="form-group">
        <label for="Subject">Add Subject</label>
        <input
          type="text"
          v-model="parameters.subject"
          id="Subject"
          class="text-feild"
          placeholder="Enter Email Subject"
          required
        />
      </div>
      <div class="form-group">
        <label for="EmailContent">Email</label>
        <textarea
          name="Email-Content"
          id="EmailContent"
          v-model="parameters.emailBody"
          class="discription-feild"
          placeholder="Write Email Here"
          required
        ></textarea>
        <div class="Dorpdown-div">
          <!-- Dropdown for adding ingredients -->
          <div class="theme-popup">
            <input type="checkbox" id="checkbox" />
            <label for="checkbox" class="theme-popup__button">
              Add Ingredients
            </label>
            <div class="theme-popup__list-container">
              <ul class="theme-popup__list">
                <li>
                  <button
                    type="button"
                    @click="addIngredient(' {inside_temperature} ')"
                    class="ingredient-button"
                  >
                    Inside Temp
                  </button>
                </li>
                <li>
                  <button
                    type="button"
                    @click="addIngredient(' {outside_temperature} ')"
                    class="ingredient-button"
                  >
                    Outside Temp
                  </button>
                </li>
                <li>
                  <button
                    type="button"
                    @click="addIngredient(' {weather_condition} ')"
                    class="ingredient-button"
                  >
                    Condition
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <button type="submit" class="button-2 mt-4">Create</button>
    </div>
  </form>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios"; // Import Axios for making HTTP requests

// Reactive variables
const actionName = ref(""); // Action name
const parameters = ref({
  emailAddress: "", // Email address
  subject: "", // Email subject
  emailBody: "", // Email body
});
const errorMessage = ref(""); // Error message for validation

// Function to add selected ingredient to the email body
const addIngredient = (ingredient) => {
  parameters.value.emailBody += ` ${ingredient}`;
};

// Function to validate input and create a new action via POST request
const createAction = async () => {
  errorMessage.value = ""; // Reset error message

  // Validation
  if (!actionName.value.trim()) {
    errorMessage.value = "Please enter a valid Action name.";
    return;
  }
  if (!parameters.value.emailAddress) {
    errorMessage.value = "Please enter a valid Email Address.";
    return;
  }
  if (!parameters.value.subject) {
    errorMessage.value = "Please enter a valid Email Subject.";
    return;
  }
  if (!parameters.value.emailBody) {
    errorMessage.value = "Please write the Email Body.";
    return;
  }

  try {
    // Prepare the payload for the POST request
    const payload = {
      service_id: 5, // Service ID for Email
      name: actionName.value,
      action_type: "Send Email", // Action type
      parameters: {
        emailAddress: parameters.value.emailAddress, // Email address
        subject: parameters.value.subject, // Email subject
        emailBody: parameters.value.emailBody, // Email body
      },
    };

    // Log the payload for debugging
    console.log("Payload:", payload);

    // Send the POST request to the API endpoint
    const response = await axios.post("http://127.0.0.1:5000/actions", payload);

    // Handle successful response
    console.log("Server Response:", response.data);
    alert("Action created successfully!");
    resetForm(); // Reset the form after successful creation
    location.reload();
  } catch (error) {
    // Handle errors
    if (error.response) {
      errorMessage.value = `Error creating action: ${
        error.response.data.message || error.response.statusText
      }`;
      console.error("Server Response:", error.response.data); // Log the full response
    } else {
      errorMessage.value = "An unexpected error occurred. Please try again later.";
    }
    console.error("Error creating action:", error);
  }
};

// Function to reset the form
const resetForm = () => {
  actionName.value = "";
  parameters.value.emailAddress = "";
  parameters.value.subject = "";
  parameters.value.emailBody = "";
};

document.addEventListener("click", (event) => {
  const dropdown = document.querySelector(".theme-popup");
  const checkbox = document.getElementById("checkbox");

  if (dropdown && checkbox && !dropdown.contains(event.target)) {
    checkbox.checked = false; // Close dropdown
  }
});


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


/* From Uiverse.io by Galahhad */
/* radio settings 👇 */

.theme-popup {
    /* total */
    --total_text_color: #e0e0e0;
    --total_font_family: Menlo, Roboto Mono, monospace;
    /* button */
    --btn_bg: #3A3A3A;
    --btn_padding: 0.5em;
    --btn_height: 2em;
    --btn_border_radius: 0.3125em;
    --btn_outline_width: 0.0625em;
    --btn_outline_color: #A0A0A0;
    --btn_outline_offset: 0.0625em;
    --btn_gap: 0.3125em;
    /* list */
    --list_padding: 0.5em;
    --list_bg: var(--btn_bg);
    --list_border_radius: var(--btn_border_radius);
    --list_gap: 0.1875em;
    --list_btn_hover_bg: #5A5656;
    --list_btn_active: #b9b9b970;
    --list_btn_border_radius: 0.25em;
    --list_btn_padding: 0.35em 1em;
    --list_btn_gap: 0.4375em;
    --list_btn_outline_width: 0.0625em;
    --list_btn_outline_color: rgb(212, 210, 210);
    --list_offset: 0.35em;
    --list_btn_font_size: 14px;
    --list_position_left: 0;
    --list_position_right: unset;
    /* 👆 if you want to change sides just switch one property */
    /* from properties to "unset" and the other to 0 */
}

.theme-popup__button .theme-popup__icons svg,
#light,
#dark,
#default,
#checkbox,
.theme-popup__list-container {
    width: 100%;
    display: none;
}

.Dorpdown-div {
    display: flex;
    justify-content: end;
    align-items: center;
    width: 100%;
}

.theme-popup {
    color: var(--ui-1);
    position: relative;
    user-select: none;
}

.theme-popup__list-container {
    position: absolute;
    left: var(--list_position_left);
    right: var(--list_position_right);
    top: calc(var(--btn_height) + var(--list_offset));
}

.theme-popup__icons {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
}

.theme-popup__button {
    line-height: var(--btn_height);
    background-color: var(--color-background-2);
    padding: 0 var(--btn_padding);
    display: inline-flex;
    align-items: center;
    column-gap: var(--btn_gap);
    border-radius: var(--btn_border_radius);
    border: none;
    color: inherit;
    font-family: inherit;
    outline: none;
    font-weight: bold;
}

.theme-popup__list {
    margin: 0;
    list-style-type: none;
    padding: var(--list_padding);
    border-radius: var(--list_border_radius);
    background-color: var(--list_bg);
    display: flex;
    flex-direction: column;
    row-gap: var(--list_gap);
}

.theme-popup__list label {
    display: flex;
    align-items: center;
    justify-content: start;
    column-gap: var(--list_btn_gap);
    padding: var(--list_btn_padding);
    border-radius: var(--list_btn_border_radius);
    white-space: nowrap;
}

/* actions */

#checkbox:checked~.theme-popup__button {
    outline: var(--btn_outline_width) solid var(--btn_outline_color);
    outline-offset: var(--btn_outline_offset);
}

#checkbox:checked~.theme-popup__list-container {
    display: block;
}

.theme-popup__list label:hover,
.theme-popup__button:hover,
#checkbox:checked~.theme-popup__button {
    background-color: var(--list_btn_hover_bg);
}

#default:checked~.theme-popup__list-container label[for="default"],
#light:checked~.theme-popup__list-container label[for="light"],
#dark:checked~.theme-popup__list-container label[for="dark"] {
    background-color: var(--list_btn_active);
    outline: var(--list_btn_outline_width) solid var(--list_btn_outline_color);
}

#default:checked~label svg.default,
#light:checked~label svg.sun,
#dark:checked~label svg.moon {
    display: block;
}


/* Optional styling for buttons */
.ingredient-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  width: 100%;
  color: var(--ui-1);
  font-weight: 600;
  padding: 5px 0px;
}

.ingredient-button:hover {
  background-color: #818181;
  transition: 0.5s;
}

</style>