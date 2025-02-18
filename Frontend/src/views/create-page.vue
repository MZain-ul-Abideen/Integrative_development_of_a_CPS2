<template>
  <div class="main-wrapper">
    <div class="main-div-card">
      <!-- Global effects -->
      <div class="affect-global-blue1"></div>
      <div class="affect-global-blue2"></div>
      <div class="affect-global-blue3"></div>
      <div class="affect-global-yellow1"></div>
      <div class="affect-global-yellow2"></div>
      <div class="affect-global-lightblue1"></div>
      <div class="hover-effect"></div>
      <form action="" class="content">
        <div class="d-flex align-items-center justify-content-between mb-5">
          <h5 class="mb-4">Create</h5>
          <button type="button" class="button-2" :hidden="!isRuleAndActionSelected" @click="createRule">
            Create Rule
          </button>
        </div>
        <div class="ifthan-wrapper">
          <!-- If This Section -->
          <div class="ifthan-div">
            <div class="ifthan-header">
              <div class="ifthan-header-card">
                <span>If This</span>
                <div class="d-flex">
                  <div class="px-2">
                    <a href="#" @click.prevent="toggleIfCards">
                      <img :src="add" alt="Add" />
                    </a>
                  </div>
                </div>
              </div>
              <hr v-if="selectedService && selectedTrigger" />
              <div v-if="selectedService && selectedTrigger" class="selected-servce">
                <span><span class="fw-bold">Service: </span>{{ selectedService }}</span>
                <span><span class="fw-bold">Trigger: </span>{{
                  selectedTrigger
                }}</span>
              </div>
            </div>
            <div class="ifthan-cards-div" v-if="showCards1">
              <a href="#" class="ifthan-card" @click.prevent="openTriggerModal('Temperature')">
                <img :src="weatherimage" class="weather-img" />
                <span>Weather</span>
              </a>
              <a href="#" class="ifthan-card" @click.prevent="openTriggerModal('Timer')">
                <img :src="timer" class="weather-img" />
                <span>Timer</span>
              </a>
              <a href="#" class="ifthan-card" @click.prevent="openTriggerModal('Sensor Temperature')">
                <img :src="IoT" class="weather-img" />
                <span>IoT Device</span>
              </a>
            </div>
          </div>
          <!-- Arrow separator -->
          <div class="mx-5 my-4">
            <img :src="arrow" alt="" />
          </div>
          <!-- Then That Section -->
          <div class="ifthan-div">
            <div class="ifthan-header">
              <div class="ifthan-header-card">
                <span>Then That</span>
                <div class="d-flex">
                  <div class="px-2">
                    <a href="#" @click.prevent="toggleThenCards">
                      <img :src="add" alt="Add" />
                    </a>
                  </div>
                </div>
              </div>
              <hr v-if="selectedActionService && selectedAction" />
              <div v-if="selectedActionService && selectedAction" class="selected-servce">
                <span><span class="fw-bold">Service: </span>{{
                  selectedActionService
                }}</span>
                <span><span class="fw-bold">Action: </span>{{
                  selectedAction
                }}</span>
              </div>
            </div>
            <div class="ifthan-cards-div" v-if="showCards2">
              <a href="#" class="ifthan-card" @click.prevent="openActionModal('Building Automation')">
                <img :src="buildingtemp" class="weather-img" />
                <span>Building Automation</span>
              </a>
              <a href="#" class="ifthan-card" @click.prevent="openActionModal('Email')">
                <img :src="email" class="weather-img" />
                <span>Email</span>
              </a>
              <a href="#" class="ifthan-card" @click.prevent="openActionModal('LED')">
                <img :src="IoT" class="weather-img" />
                <span>IoT Device</span>
              </a>
            </div>
          </div>
        </div>
      </form>
    </div>
    <!-- Modals -->
    <ModalTrigger ref="modalTriggerRef" @trigger-selected="handleTriggerSelection" />
    <ModalAction ref="modalActionRef" @action-selected="handleActionSelection" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router'; // Import Vue Router
import ModalTrigger from '@/components/trigger-modal.vue';
import ModalAction from '@/components/action-modal.vue';
import api from '@/api.js'; // Import API utility

// Assets
import add from '@/assets/svgs/add.svg';
import edit from '@/assets/svgs/edit.svg';
import del from '@/assets/svgs/delete.svg';
import arrow from '@/assets/svgs/arrow.svg';
import weatherimage from '@/assets/pictures/weather.png';
import buildingtemp from '@/assets/pictures/building-temp.png';
import IoT from '@/assets/pictures/IoT.png';
import email from '@/assets/pictures/email.png';
import timer from '@/assets/pictures/time.png';

// Initialize Vue Router
const router = useRouter();

// Refs
const showCards1 = ref(false); // Controls visibility of "If This" cards
const showCards2 = ref(false); // Controls visibility of "Then That" cards
const modalTriggerRef = ref(null);
const modalActionRef = ref(null);

// Selected service and trigger/action
const selectedService = ref('');
const selectedTrigger = ref('');
const selectedActionService = ref('');
const selectedAction = ref('');

// Hidden fields for rule_id, rule_name, action_id, and action_name
const ruleId = ref(null);
const ruleName = ref('');
const actionId = ref(null);
const actionName = ref('');

// Computed property to check if both rule and action are selected
const isRuleAndActionSelected = computed(() => {
  return ruleId.value && actionId.value;
});

// Toggle card visibility
function toggleIfCards() {
  showCards1.value = !showCards1.value;
}
function toggleThenCards() {
  showCards2.value = !showCards2.value;
}

// Open modals
function openTriggerModal(service) {
  modalTriggerRef.value?.openModal(service);
}
function openActionModal(service) {
  modalActionRef.value?.openModal(service);
}

// Handle selections
function handleTriggerSelection({ service, trigger }) {
  selectedService.value = service;
  selectedTrigger.value = trigger;
  fetchRuleId(service, trigger); // Fetch rule ID and name
}
function handleActionSelection({ service, action }) {
  selectedActionService.value = service;
  selectedAction.value = action;
  fetchActionId(service, action); // Fetch action ID and name
}

// API utility function to fetch rule ID
const fetchRuleId = async (service, trigger) => {
  try {
    const response = await api.getData(`rules?service=${service}&name=${trigger}`);
    if (response.length > 0) {
      const rule = response.find(r => r.name === trigger); // Ensure exact match
      if (rule) {
        ruleId.value = rule.id;
        ruleName.value = rule.name;
      } else {
        console.error("No rule found with the exact name:", trigger);
        alert("No rule found for the selected trigger. Please check your selection.");
      }
    } else {
      console.error("No rules found for the given service and trigger.");
      alert("No rule found for the selected trigger. Please check your selection.");
    }
  } catch (error) {
    console.error("Error fetching rule ID:", error);
    alert("Failed to fetch rule ID. Please try again later.");
  }
};

// API utility function to fetch action ID
const fetchActionId = async (service, action) => {
  try {
    const response = await api.getData(`actions?service=${service}&name=${action}`);
    if (response.length > 0) {
      const actionData = response.find(a => a.name === action); // Ensure exact match
      if (actionData) {
        actionId.value = actionData.id;
        actionName.value = actionData.name;
      } else {
        console.error("No action found with the exact name:", action);
        alert("No action found for the selected action. Please check your selection.");
      }
    } else {
      console.error("No actions found for the given service and action.");
      alert("No action found for the selected action. Please check your selection.");
    }
  } catch (error) {
    console.error("Error fetching action ID:", error);
    alert("Failed to fetch action ID. Please try again later.");
  }
};

// Submit the form
async function createRule() {
  if (!isRuleAndActionSelected.value) {
    alert("Please select both a trigger and an action.");
    return;
  }

  try {
    const payload = {
      rule_id: ruleId.value,
      action_id: actionId.value,
    };


    const response = await api.postData('link-rule-action', payload);

    alert(
      `Rule Created Successfully!`
    );

    router.push('/rules').then(() => {
      location.reload();
    });

  } catch (error) {
    if (error.response) {
      alert(
        `Error linking rule and action: ${error.response.data.message || error.response.statusText}`
      );
      console.error("Server Response:", error.response.data);
    } else {
      alert("An unexpected error occurred. Please try again later.");
    }
    console.error("Error linking rule and action:", error);
  }
}
</script>


<style scoped>
.content {
  width: 100%;
  padding: 2rem;
  height: 100%;
}

.ifthan-wrapper {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: start;
}

.ifthan-div {
  height: 100%;
  width: 100%;
}

.ifthan-header {
  border: 1px solid var(--ui-3);
  border-radius: 20px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  padding: 2rem;
}

.ifthan-header-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ifthan-header-card span {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-1);
}

.selected-servce {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ifthan-cards-div {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  /* 2 cards in a row */
  gap: 1rem;
  /* Gap between cards */
  height: 100px;
  margin-top: 1rem;
}

.ifthan-card {
  min-height: 175px;
  border: 1px solid var(--ui-3);
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 5rem;
  text-decoration: none;
  color: var(--ui-1);
  text-transform: capitalize;
  animation: fadeIn 0.2s ease-in-out;
}

.ifthan-card:hover {
  box-shadow: 0 0 40px 0 rgba(0, 0, 0, 0.267);
  transition: 0.3s;
}

.ifthan-card img {
  width: auto;
  height: 75px;
}

.ifthan-card span {
  font-size: 1.2rem;
  font-weight: 500;
  color: var(--text-1);
  margin-top: 1rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>