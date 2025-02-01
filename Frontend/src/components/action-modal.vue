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
        <span>{{ title }}</span>

        <!-- Show AddAction component when showAddAction is true -->
        <AddAction v-if="showAddAction" />

        <!-- Show dynamic action options based on the selected service -->
        <div class="action-card-wrapper" v-if="!showAddAction">
          <div v-for="(action, index) in selectedActions" :key="index" class="action-card">
            <div class="action-card-header">
              <span>{{ action.name }}</span>
            </div>
            <div class="action-card-body">
              <p>{{ action.description }}</p>
            </div>
          </div>
          <button class="action-card action-card-add" @click="showAddAction = true">
            <img :src="add" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import cross from '@/assets/svgs/cross.svg';
import add from '@/assets/svgs/add.svg';
import AddAction from '@/components/sub-components/addAction-component.vue';

// Service-specific action options
const actionOptions = {
  "Temperature": [
    { name: "Set Threshold", description: "Set a threshold for temperature control" },
    { name: "Adjust Heating", description: "Increase or decrease the heating" }
  ],
  "Building Automation": [
    { name: "Turn On Lights", description: "Activate the lights in a room" },
    { name: "Lock Doors", description: "Secure the doors automatically" }
  ],
  "Sensor Temperature": [
    { name: "Activate Cooling", description: "Turn on cooling system when temperature rises" },
    { name: "Trigger Alarm", description: "Sound an alarm if temperature is critical" }
  ],
  "Email": [
    { name: "Send Email", description: "Send an automated email notification" },
    { name: "Mark as Read", description: "Mark incoming emails as read" }
  ],
  "Timer": [
    { name: "Start Countdown", description: "Start a countdown timer" },
    { name: "Repeat Task", description: "Schedule a recurring task" }
  ]
};

const isVisible = ref(false);
const title = ref('');
const showAddAction = ref(false);

// Dynamically get the relevant actions based on the selected service
const selectedActions = computed(() => {
  return actionOptions[title.value] || [];
});

function openModal(modalTitle) {
  title.value = modalTitle;
  isVisible.value = true;
  showAddAction.value = false; // Reset to default state when opening
}

function closeModal() {
  isVisible.value = false;
  showAddAction.value = false; // Reset when closing
}

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
