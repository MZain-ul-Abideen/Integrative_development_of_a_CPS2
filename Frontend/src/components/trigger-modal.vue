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
        
        <AddTrigger v-if="showAddTrigger" :selectedService="title" :selectedTrigger="selectedTrigger" />

        <div class="trigger-card-wrapper" v-if="!showAddTrigger">
          <a href="#" v-for="(trigger, index) in selectedTriggers" 
             :key="index" class="trigger-card">
            <div class="trigger-card-header">
              <span>{{ trigger.name }}</span>
            </div>
            <div class="trigger-card-body">
              <p>{{ trigger.description }}</p>
            </div>
          </a>
          <button class="trigger-card trigger-card-add" @click="showAddTrigger = true">
            <img :src="add" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits } from 'vue';
import cross from '@/assets/svgs/cross.svg';
import add from '@/assets/svgs/add.svg';
import AddTrigger from '@/components/sub-components/addTrigger-component.vue';

const triggerOptions = {
  "Temperature": [
    { name: "Threshold", description: "Trigger when temperature crosses a threshold" },
    { name: "Fluctuation", description: "Trigger when temperature fluctuates rapidly" }
  ],
  "Building Automation": [
    { name: "Motion Detected", description: "Trigger when motion is detected" },
    { name: "Light On", description: "Trigger when a light turns on" }
  ],
  "Sensor Temperature": [
    { name: "High Temp", description: "Trigger when sensor detects high temperature" },
    { name: "Low Temp", description: "Trigger when sensor detects low temperature" }
  ],
  "Email": [
    { name: "Received", description: "Trigger when an email is received" },
    { name: "Sent", description: "Trigger when an email is sent" }
  ],
  "Timer": [
    { name: "Countdown", description: "Trigger when a countdown reaches zero" },
    { name: "Interval", description: "Trigger at regular intervals" }
  ]
};

const isVisible = ref(false);
const title = ref('');
const showAddTrigger = ref(false);
const selectedTrigger = ref('');
const emit = defineEmits(['trigger-selected']);

const selectedTriggers = computed(() => {
  return triggerOptions[title.value] || [];
});

function openModal(modalTitle) {
  title.value = modalTitle;
  isVisible.value = true;
  showAddTrigger.value = false;
  selectedTrigger.value = '';
}

function closeModal() {
  isVisible.value = false;
  showAddTrigger.value = false;
  selectedTrigger.value = '';
}

function selectTrigger(triggerName) {
  selectedTrigger.value = triggerName;
  showAddTrigger.value = true;
}

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