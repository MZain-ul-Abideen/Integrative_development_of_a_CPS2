<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import ModalTrigger from '@/components/trigger-modal.vue';
import ModalAction from '@/components/action-modal.vue';

import add from '@/assets/svgs/add.svg';
import edit from '@/assets/svgs/edit.svg';
import del from '@/assets/svgs/delete.svg';
import arrow from '@/assets/svgs/arrow.svg';

import weatherimage from '@/assets/pictures/weather.png';
import buildingtemp from '@/assets/pictures/building-temp.png';
import IoT from '@/assets/pictures/IoT.png';
import email from '@/assets/pictures/email.png';
import timer from '@/assets/pictures/time.png';

// Refs
const showCards1 = ref(false);
const showCards2 = ref(false);
const modalTriggerRef = ref(null);
const modalActionRef = ref(null);

// Selected service and trigger/action
const selectedService = ref('');
const selectedTrigger = ref('');
const selectedActionService = ref('');
const selectedAction = ref('');


// Define the functions directly in the setup block
function handleMouseMove(event) {
  const card = event.currentTarget;
  const hoverEffect = card.querySelector(".hover-effect");

  // Get card's bounding box
  const rect = card.getBoundingClientRect();

  // Calculate mouse position within the card
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  // Position the shadow
  hoverEffect.style.top = `${y - 100}px`; // Offset to center the shadow
  hoverEffect.style.left = `${x - 100}px`;
  hoverEffect.style.opacity = 1; // Show the shadow
}

function handleMouseLeave(event) {
  const hoverEffect = event.currentTarget.querySelector(".hover-effect");
  hoverEffect.style.opacity = 0; // Hide the shadow on mouse leave
}


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
}

function handleActionSelection({ service, action }) {
    selectedActionService.value = service;
    selectedAction.value = action;
}
</script>

<template>
  <div class="main-wrapper">
    <div
      class="main-div-card"
      @mousemove="handleMouseMove"
      @mouseleave="handleMouseLeave"
    >
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
          <button type="button" class="button-2" @click="createRule">Create Rule</button>
        </div>

        <div class="ifthan-wrapper">
          <!-- If This Section -->
          <div class="ifthan-div">
            <div class="ifthan-header">
              <div class="ifthan-header-card">
                <span>If This</span>
                <div class="d-flex">
                  <div class="px-2">
                    <!-- Add button for If This -->
                    <a href="#" @click.prevent="toggleIfCards">
                      <img :src="add">
                    </a>
                  </div>
                  <div class="px-2">
                    <!-- Delete button -->
                    <a href="#"><img :src="del"></a>
                  </div>
                </div>
              </div>
              <hr v-if="selectedService && selectedTrigger">
              <div v-if="selectedService && selectedTrigger" class="selected-servce">
                <span><span class="fw-bold">Service: </span>{{ selectedService }}</span>
                <span><span class="fw-bold">Trigger: </span>{{ selectedTrigger }}</span>
              </div>
            </div>
            <!-- Cards for If This -->
            <div class="ifthan-cards-div" v-if="showCards1">
              <a href="#" class="ifthan-card" @click.prevent="openTriggerModal('Temperature')">
                <img :src="weatherimage" class="weather-img">
                <span>Weather</span>
              </a>
              <a href="#" class="ifthan-card" @click.prevent="openTriggerModal('Timer')">
                <img :src="timer" class="weather-img">
                <span>Timer</span>
              </a>
              <a href="#" class="ifthan-card" @click.prevent="openTriggerModal('Sensor Temperature')">
                <img :src="IoT" class="weather-img">
                <span>IoT Device</span>
              </a>
            </div>
          </div>

          <!-- Arrow separator -->
          <div class="mx-5 my-4">
            <img :src="arrow" alt="">
          </div>

          <!-- Then That Section -->
          <div class="ifthan-div">
            <div class="ifthan-header">
              <div class="ifthan-header-card">
                <span>Then That</span>
                <div class="d-flex">
                  <div class="px-2">
                    <!-- Add button for Then That -->
                    <a href="#" @click.prevent="toggleThenCards">
                      <img :src="add">
                    </a>
                  </div>
                  <div class="px-2">
                    <!-- Delete button -->
                    <a href="#"><img :src="del"></a>
                  </div>
                </div>
              </div>
              <hr v-if="selectedActionService && selectedAction">
              <div v-if="selectedActionService && selectedAction" class="selected-servce">
                <span><span class="fw-bold">Service: </span>{{ selectedActionService }}</span>
                <span><span class="fw-bold">Action: </span>{{ selectedAction }}</span>
              </div>
            </div>
            <!-- Cards for Then That -->
            <div class="ifthan-cards-div" v-if="showCards2">
              <a href="#" class="ifthan-card" @click.prevent="openActionModal('Building Automation')">
                <img :src="buildingtemp" class="weather-img">
                <span>Building Automation</span>
              </a>
              <a href="#" class="ifthan-card" @click.prevent="openActionModal('Email')">
                <img :src="email" class="weather-img">
                <span>Email</span>
              </a>
              <a href="#" class="ifthan-card" @click.prevent="openActionModal('LED')">
                <img :src="IoT" class="weather-img">
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
    grid-template-columns: repeat(2, 1fr); /* 2 cards in a row */
    gap: 1rem; /* Gap between cards */
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