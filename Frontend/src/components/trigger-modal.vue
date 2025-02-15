<template>
  <div v-if="isVisible" class="modal-overlay">
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
        <!-- Trigger cards -->
        <div class="trigger-card-wrapper" v-if="!showAddTrigger">
          <!-- Display filtered rules -->
          <a
            href="#"
            v-for="(rule, index) in selectedTriggers"
            :key="'rule-' + index"
            class="trigger-card"
            @click.prevent="selectTrigger(rule)"
          >
            <!-- <a class="dlt-list-item">
              <img :src="del" />
            </a> -->
            <div class="trigger-card-header">
              <span>{{ rule.name }}</span>
            </div>
          </a>
          <!-- No rules message -->
          <div v-if="selectedTriggers.length === 0" class="no-rules-message">
            No rules available for this category.
          </div>
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
import { ref, computed, onMounted } from 'vue';
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
const createdTriggers = ref([]); // Stores created rules

// Computed
const selectedTriggers = computed(() => {
  const category = title.value;
  return createdTriggers.value.filter(rule => 
    rule.category === category
  );
});

// Emits
const emit = defineEmits(['trigger-selected']);

// Methods
function openModal(modalTitle) {
  title.value = modalTitle; // Ensure modalTitle is one of "Temperature", "Timer", or "Sensor Temperature"
  isVisible.value = true;
  showAddTrigger.value = false;
}

function closeModal() {
  isVisible.value = false;
  showAddTrigger.value = false;
}

function selectTrigger(trigger) {
  emit('trigger-selected', { service: title.value, trigger: trigger.name });
  closeModal();
}

function handleTriggerCreated(newTrigger) {
  createdTriggers.value.push(newTrigger);
  showAddTrigger.value = false;
}

// Fetch rules from the API on component mount
async function fetchRules() {
  try {
    const response = await api.getData('rules'); // Fetch data from the API

    // Debugging: Log the raw API response
    console.log("API Response:", response);

    // Group rules by service ID and map them to categories
    const groupedRules = response.map(rule => ({
      ...rule,
      category: serviceIdToCategory[rule.service.id] || "Unknown"
    })).filter(rule => rule.category !== "Unknown"); // Exclude rules with unknown categories

    // Debugging: Log the grouped rules
    console.log("Grouped Rules:", groupedRules);

    createdTriggers.value = groupedRules; // Update the createdTriggers array
  } catch (error) {
    console.error("Error fetching rules:", error);
  }
}

// Call fetchRules when the component is mounted
onMounted(fetchRules);

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