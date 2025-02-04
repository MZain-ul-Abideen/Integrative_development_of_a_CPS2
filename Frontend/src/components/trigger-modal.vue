<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-content-wrapper">
      <div class="modal-content-header">
        <span v-if="!showAddTrigger">Choose a Rule</span>
        <span v-else>Create a new Rule</span>
        <button @click="closeModal" class="btn">
          <img :src="cross" />
        </button>
      </div>
      <div class="modal-content-div">
        <span v-if="!showAddTrigger"> {{ title }}</span>
        
        <!-- AddTrigger component -->
        <AddTrigger 
          v-if="showAddTrigger" 
          :selectedService="title" 
          @trigger-created="handleTriggerCreated"
        />

        <!-- Trigger cards -->
        <div class="trigger-card-wrapper" v-if="!showAddTrigger">
          <!-- Display created rules -->
          <a 
            href="#" 
            v-for="(trigger, index) in createdTriggers" 
            :key="index" 
            class="trigger-card"
            @click.prevent="selectTrigger(trigger)"
          >
            <div class="trigger-card-header">
              <span>{{ trigger.name }}</span>
            </div>
            <div class="trigger-card-body">
              <p>{{ trigger.description }}</p>
            </div>
          </a>

          <!-- Display default trigger options -->
          <a 
            href="#" 
            v-for="(trigger, index) in selectedTriggers" 
            :key="index" 
            class="trigger-card"
            @click.prevent="selectTrigger(trigger)"
          >
            <div class="trigger-card-header">
              <span>{{ trigger.name }}</span>
            </div>
            <div class="trigger-card-body">
              <p>{{ trigger.description }}</p>
            </div>
          </a>

          <!-- Add new rule button -->
          <button class="trigger-card trigger-card-add" @click="showAddTrigger = true">
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
import AddTrigger from '@/components/sub-components/addTrigger-component.vue';

// Trigger options
const triggerOptions = {
  "Temperature": [
    { name: "Threshold", description: "Trigger when temperature crosses a threshold" },
    { name: "Fluctuation", description: "Trigger when temperature fluctuates rapidly" }
  ],
  "Sensor Temperature": [
    { name: "High Temp", description: "Trigger when sensor detects high temperature" },
    { name: "Low Temp", description: "Trigger when sensor detects low temperature" }
  ],
  "Timer": [
    { name: "Countdown", description: "Trigger when a countdown reaches zero" },
    { name: "Interval", description: "Trigger at regular intervals" }
  ]
};

// Refs
const isVisible = ref(false);
const title = ref('');
const showAddTrigger = ref(false);
const createdTriggers = ref([]); // Stores created rules

// Computed
const selectedTriggers = computed(() => {
  return triggerOptions[title.value] || [];
});

// Emits
const emit = defineEmits(['trigger-selected']);

// Methods
function openModal(modalTitle) {
  title.value = modalTitle;
  isVisible.value = true;
  showAddTrigger.value = false;
}

function closeModal() {
  isVisible.value = false;
  showAddTrigger.value = false;
}

function selectTrigger(trigger) {
  // Emit the selected trigger to the parent component
  emit('trigger-selected', { service: title.value, trigger: trigger.name });
  closeModal();
}

function handleTriggerCreated(newTrigger) {
  // Append the new trigger to the createdTriggers list
  createdTriggers.value.push(newTrigger);
  showAddTrigger.value = false; // Hide the AddTrigger component
}

// Expose openModal to parent
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

.trigger-card-wrapper {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.trigger-card {
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
  color: var(--ui-1);
  text-decoration: none;
}

.trigger-card-add {
  background: transparent;
  border: 1px dashed var(--ui-1);
}
</style>