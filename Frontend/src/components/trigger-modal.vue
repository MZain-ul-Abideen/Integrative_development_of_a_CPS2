<template>
  <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content-wrapper">
      <div class="modal-content-header">
        <span v-if="!showAddTrigger">Choose a Trigger</span>
        <span v-else>Create a new Trigger</span>
        <button @click="closeModal" class="btn">
          <img :src="cross" />
        </button>
      </div>
      <div class="modal-content-div">
        <span v-if="!showAddTrigger">{{ title }}</span>
        <!-- AddTrigger component -->
        <AddTrigger 
          v-if="showAddTrigger" 
          :selectedService="title" 
          @trigger-created="handleTriggerCreated" 
        />
        <!-- Trigger cards inside a scrollable iframe-like div -->
        <div class="trigger-card-container" v-if="!showAddTrigger">
          <div class="trigger-card-wrapper">
            <!-- Add new rule button -->
            <button class="trigger-card trigger-card-add" @click="showAddTrigger = true">
              <img :src="add" />
            </button>
            <!-- Display filtered rules -->
            <div 
              class="trigger-card" 
              v-for="(rule, index) in selectedTriggers" 
              :key="'rule-' + index"
            >
              <div class="dlt-btn-dev">
                <!-- Delete button -->
                <a href="#" @click.prevent="deleteRule(rule.id)">
                  <img :src="cross" />
                </a>
              </div>
              <div class="trigger-card-select">
                <!-- Select rule -->
                <a href="#" @click.prevent="selectTrigger(rule)">
                  <div class="trigger-card-header">
                    <span>{{ rule.name }}</span>
                  </div>
                </a>
              </div>
            </div>
            <!-- No rules message -->
            <div v-if="selectedTriggers.length === 0" class="no-rules-message">
              No rules available for this category.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import cross from '@/assets/svgs/cross.svg';
import add from '@/assets/svgs/add.svg';
import del from '@/assets/svgs/delete.svg';
import AddTrigger from '@/components/sub-components/addTrigger-component.vue';
import api from '@/api'; // Import your Axios utility

// Service ID to Category Mapping
const serviceIdToCategory = {
  1: "Temperature",
  2: "Timer",
  3: "Sensor Temperature"
};

// Refs
const isVisible = ref(false);
const title = ref('');
const showAddTrigger = ref(false);
const createdTriggers = ref([]);

// Computed
const selectedTriggers = computed(() => {
  const category = title.value;
  return createdTriggers.value
    .filter(rule => rule.category === category)
    .sort((a, b) => (a.id > b.id ? -1 : 1)); // Sort by ID in descending order
});

// Emits
const emit = defineEmits(['trigger-selected']);

// Methods
function openModal(modalTitle) {
  title.value = modalTitle;
  isVisible.value = true;
  showAddTrigger.value = false;
  document.addEventListener("keydown", handleKeyPress);
}

function closeModal() {
  isVisible.value = false;
  showAddTrigger.value = false;
  document.removeEventListener("keydown", handleKeyPress);
}

function selectTrigger(trigger) {
  emit('trigger-selected', { service: title.value, trigger: trigger.name });
  closeModal();
}

function handleTriggerCreated(newTrigger) {
  createdTriggers.value.push(newTrigger); // Add the new trigger to the list
  showAddTrigger.value = false; // Switch back to "Choose a Trigger" state
  createdTriggers.value.sort((a, b) => (a.id > b.id ? -1 : 1)); // Re-sort the triggers
}

// Close modal when pressing Escape key
function handleKeyPress(event) {
  if (event.key === "Escape") {
    closeModal();
  }
}

// Fetch rules from the API on component mount
async function fetchRules() {
  try {
    const response = await api.getData('rules'); // Fetch rules from the backend
    console.log("API Response:", response);

    const groupedRules = response.map(rule => ({
      ...rule,
      category: serviceIdToCategory[rule.service.id] || "Unknown"
    })).filter(rule => rule.category !== "Unknown"); // Exclude rules with unknown categories

    groupedRules.sort((a, b) => (a.id > b.id ? -1 : 1)); // Sort by ID in descending order
    console.log("Grouped and Sorted Rules:", groupedRules);

    createdTriggers.value = groupedRules; // Update the local state with fetched rules
  } catch (error) {
    console.error("Error fetching rules:", error);
  }
}

// Delete a rule by ID
async function deleteRule(ruleId) {
  try {
    // Confirm deletion with the user
    if (!confirm(`Are you sure you want to delete the rule with ID ${ruleId}?`)) {
      return;
    }

    // Debugging: Log the rule ID being deleted
    console.log("Deleting Rule with ID:", ruleId);

    // Send DELETE request to the backend
    const response = await api.deleteData(`rules/${ruleId}`);
    console.log("Server Response:", response);

    // Remove the rule from the local state
    createdTriggers.value = createdTriggers.value.filter(rule => rule.id !== ruleId);

    // Notify via console instead of alert
    console.log("Rule deleted successfully.");

    // Refresh the page after deletion
  } catch (error) {
    console.error("Error deleting rule:", error);
  }
  location.reload(); // Reload the page to reflect changes
}

// Call fetchRules when the component is mounted
onMounted(fetchRules);

// Expose openModal to parent component
defineExpose({ openModal });
</script>


<style scoped>
.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content-wrapper {
  border-radius: 30px;
  background-color: var(--card-1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 2rem;
  text-align: center;
  width: 50%;
  min-height: 800px;
}

.modal-content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.modal-content-header span {
  font-size: 1.3rem;
  font-weight: 600;
  text-transform: capitalize;
}

.modal-content-header .btn {
  background: none;
  border: none;
  cursor: pointer;
}

.modal-content-div {
  width: 100%;
}

.modal-content-div span {
  font-size: 18px;
  font-weight: 600;
  text-transform: capitalize;
}

/* Scrollable iframe-like container */
.trigger-card-container {
  max-height: 600px;
  /* Adjust the height as needed */
  overflow-y: auto;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
}

/* Grid layout inside the scrollable container */
.trigger-card-wrapper {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.trigger-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-top: 1rem;
  background: var(--color-background);
  min-height: 120px;
}

.trigger-card-select {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.trigger-card a {
  cursor: pointer;
  color: var(--ui-1);
  text-decoration: none;
}

.dlt-btn-dev {
  display: flex;
  justify-content: end;
  position: relative;
  padding: 0.7rem;
}

.trigger-card-add {
  background: transparent;
  border: 1px dashed var(--ui-1);
}

.no-rules-message {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
}


/* For WebKit browsers (Chrome, Safari) */
.trigger-card-container::-webkit-scrollbar {
  width: 8px;
  /* Scrollbar width */
  border-radius: 4px;
}

/* Scrollbar track */
.trigger-card-container::-webkit-scrollbar-track {
  background: var(--ui-1);
  /* Light grey background */
  border-radius: 4px;
}

/* Scrollbar handle */
.trigger-card-container::-webkit-scrollbar-thumb {
  background: var(--color-background);
  /* Dark grey handle */
  border-radius: 4px;
}

/* Scrollbar handle on hover */
.trigger-card-container::-webkit-scrollbar-thumb:hover {
  background: var(--color-background);
  /* Darker grey on hover */
}

/* For Firefox */
.trigger-card-container {
  scrollbar-width: thin;
  /* Makes scrollbar thinner */
  scrollbar-color: var(--ui-1) var(--color-background);
  /* Thumb color and track color */
}
</style>
