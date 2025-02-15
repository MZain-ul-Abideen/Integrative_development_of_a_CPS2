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
        <!-- Show AddAction component when showAddAction is true -->
        <AddAction v-if="showAddAction" :selectedService="title" @action-created="handleActionCreated" />
        <!-- Show dynamic action options based on the selected service -->
        <div class="action-card-wrapper" v-if="!showAddAction">
          <!-- Display default action options -->
          <div
            v-for="(action, index) in selectedActions"
            :key="'action-' + index"
            class="action-card"
            @click="selectAction(action)"
          >
            <!-- <div class="dlt-list-item">
              <img :src="del" />
            </div> -->
            <div class="action-card-header">
              <span>{{ action.name }}</span>
            </div>
          </div>
          <!-- No actions message -->
          <div v-if="selectedActions.length === 0" class="no-actions-message">
            No actions available for this service.
          </div>
          <!-- Add new action button -->
          <button class="action-card action-card-add" @click="showAddAction = true">
            <img :src="add" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import cross from '@/assets/svgs/cross.svg';
import add from '@/assets/svgs/add.svg';
import del from '@/assets/svgs/delete.svg';
import AddAction from '@/components/sub-components/addAction-component.vue';
import api from '@/api'; // Import your Axios utility

// Service ID to Service Name Mapping
const serviceIdToName = {
  4: "Building Automation",
  5: "Email",
  6: "LED"
};

// Refs
const isVisible = ref(false);
const title = ref('');
const showAddAction = ref(false);
const createdActions = ref([]); // Stores created actions

// Computed
const selectedActions = computed(() => {
  const serviceName = title.value;
  return createdActions.value.filter(action => 
    action.service.name === serviceName
  );
});

// Emits
const emit = defineEmits(['action-selected']);

// Methods
function openModal(modalTitle) {
  title.value = modalTitle; // Ensure modalTitle matches one of the service names
  isVisible.value = true;
  showAddAction.value = false;
}

function closeModal() {
  isVisible.value = false;
  showAddAction.value = false;
}

function selectAction(action) {
  emit('action-selected', { service: title.value, action: action.name });
  closeModal();
}

function handleActionCreated(newAction) {
  createdActions.value.push(newAction);
  showAddAction.value = false;
}

// Fetch actions from the API on component mount
async function fetchActions() {
  try {
    const response = await api.getData('actions'); // Fetch data from the API

    // Debugging: Log the raw API response
    console.log("API Response:", response);

    // Group actions by service ID and map them to service names
    const groupedActions = response.map(action => ({
      ...action,
      serviceName: serviceIdToName[action.service.id] || "Unknown"
    })).filter(action => action.serviceName !== "Unknown"); // Exclude actions with unknown services

    // Debugging: Log the grouped actions
    console.log("Grouped Actions:", groupedActions);

    createdActions.value = groupedActions; // Update the createdActions array
  } catch (error) {
    console.error("Error fetching actions:", error);
  }
}

// Call fetchActions when the component is mounted
onMounted(fetchActions);

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

.action-card-wrapper {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.action-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
  margin-top: 1rem;
  cursor: pointer;
  background: var(--color-background);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.action-card-add {
  background: transparent;
  border: 1px dashed var(--ui-1);
}
</style>