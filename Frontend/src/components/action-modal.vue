<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-content-wrapper">
      <div class="modal-content-header">
        <span v-if="!showAddAction">Choose an Action</span>
        <span v-else>Create a new Action</span>
        <button @click="closeModal" class="btn">
          <img :src="cross" />
        </button>
      </div>
      <div class="modal-content-div">
        <span v-if="!showAddAction">{{ title }}</span>
        <AddAction 
          v-if="showAddAction" 
          :selectedService="title" 
          @action-created="handleActionCreated" 
        />
        <div class="action-card-wrapper" v-if="!showAddAction">
          <button class="action-card action-card-add" @click="showAddAction = true">
            <img :src="add" />
          </button>

          <!-- Display filtered actions -->
          <div 
            v-for="(action, index) in selectedActions" 
            :key="'action-' + index" 
            class="action-card"
          >
            <div class="dlt-btn-dev">
              <!-- Delete button -->
              <a href="#" @click.prevent="deleteAction(action.id)">
                <img :src="cross" />
              </a>
            </div>
            <div class="action-card-select">
              <!-- Select action -->
              <a @click="selectAction(action)">
                <div class="action-card-header pb-4">
                  <span>{{ action.name }}</span>
                </div>
              </a>
            </div>
          </div>
          <!-- No actions message -->
          <div v-if="selectedActions.length === 0" class="no-actions-message">
            No actions available for this service.
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
import AddAction from '@/components/sub-components/addAction-component.vue';
import api from '@/api';

// Service ID to Name Mapping
const serviceIdToName = {
  4: "Building Automation",
  5: "Email",
  6: "LED"
};

// Refs
const isVisible = ref(false);
const title = ref('');
const showAddAction = ref(false);
const createdActions = ref([]);

// Computed
const selectedActions = computed(() => {
  return createdActions.value
    .filter(action => action.service.name === title.value)
    .sort((a, b) => b.id - a.id); // Sort by ID in descending order (newest first)
});

// Emits
const emit = defineEmits(['action-selected']);

// Methods
function openModal(modalTitle) {
  title.value = modalTitle;
  isVisible.value = true;
  showAddAction.value = false;
  document.addEventListener('keydown', handleKeyPress); // Listen for 'Esc' key
}

function closeModal() {
  isVisible.value = false;
  showAddAction.value = false;
  document.removeEventListener('keydown', handleKeyPress); // Remove listener when modal closes
}

function selectAction(action) {
  emit('action-selected', { service: title.value, action: action.name });
  closeModal();
}

function handleActionCreated(newAction) {
  createdActions.value.push(newAction); // Add the new action to the list
  showAddAction.value = false; // Switch back to "Choose an Action" state
  createdActions.value.sort((a, b) => b.id - a.id); // Re-sort the actions
}

// Fetch actions from the API on component mount
async function fetchActions() {
  try {
    const response = await api.getData('actions'); // Fetch actions from the backend
    console.log("API Response:", response);

    const groupedActions = response.map(action => ({
      ...action,
      serviceName: serviceIdToName[action.service.id] || "Unknown"
    })).filter(action => action.serviceName !== "Unknown"); // Exclude actions with unknown services

    groupedActions.sort((a, b) => b.id - a.id); // Sort by ID in descending order
    console.log("Grouped and Sorted Actions:", groupedActions);

    createdActions.value = groupedActions; // Update the local state with fetched actions
  } catch (error) {
    console.error("Error fetching actions:", error);
  }
}

// Delete an action by ID
async function deleteAction(actionId) {
  try {
    // Confirm deletion with the user
    if (!confirm(`Are you sure you want to delete the action with ID ${actionId}?`)) {
      return;
    }

    // Debugging: Log the action ID being deleted
    console.log("Deleting Action with ID:", actionId);

    // Send DELETE request to the backend
    const response = await api.deleteData(`actions/${actionId}`);
    console.log("Server Response:", response);

    // Remove the action from the local state
    createdActions.value = createdActions.value.filter(action => action.id !== actionId);

    // Notify via console instead of alert
    console.log("Action deleted successfully.");

    // Optionally, refresh the page to reflect changes
  } catch (error) {
    console.error("Error deleting action:", error);
  }
  location.reload(); // Reload the page after deletion
}

// Close modal when clicking outside of it
function handleClickOutside(event) {
  if (event.target.classList.contains('modal-overlay')) {
    closeModal();
  }
}

// Close modal on Esc key press
function handleKeyPress(event) {
  if (event.key === "Escape") {
    closeModal();
  }
}

// Call fetchActions when the component is mounted
onMounted(() => {
  fetchActions();
  document.addEventListener('click', handleClickOutside);
});

// Clean up event listeners when the component is unmounted
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  document.removeEventListener('keydown', handleKeyPress);
});

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

.trigger-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-top: 1rem;
  background: var(--color-background);
  min-height: 120px;
}

.action-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-top: 1rem;
  background: var(--color-background);
  min-height: 120px;
}

.action-card a {
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

.action-card-add {
  background: transparent;
  border: 1px dashed var(--ui-1);
}

.no-actions-message {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.action-card-wrapper {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-top: 1rem;

  max-height: 600px;
  /* Adjust the height as needed */
  overflow-y: auto;
  /* Enable vertical scrolling when content exceeds max height */
  padding-right: 5px;
  /* Avoid scrollbar overlapping content */
}

/* Custom Scrollbar Styling */
.action-card-wrapper::-webkit-scrollbar {
  width: 8px;
  /* Scrollbar width */
  border-radius: 4px;
}

.action-card-wrapper::-webkit-scrollbar-track {
  background: var(--ui-1);
  /* Light grey background */
  border-radius: 4px;
}

.action-card-wrapper::-webkit-scrollbar-thumb {
  background: var(--color-background);
  /* Dark grey handle */
  border-radius: 4px;
}

.action-card-wrapper::-webkit-scrollbar-thumb:hover {
  background: var(--color-background);
  /* Darker grey on hover */
}

/* Firefox Scrollbar */
.action-card-wrapper {
  scrollbar-width: thin;
  /* Makes scrollbar thinner */
  scrollbar-color: var(--ui-1) var(--color-background);
  /* Thumb color and track color */
}
</style>