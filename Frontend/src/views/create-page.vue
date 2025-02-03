
<script setup>
import { ref } from 'vue';
import ModalTrigger from '@/components/trigger-modal.vue';
import ModalAction from '@/components/action-modal.vue';

import add from '@/assets/svgs/add.svg';
import edit from '@/assets/svgs/edit.svg';
import del from '@/assets/svgs/delete.svg';
import arrow from '@/assets/svgs/arrow.svg';

import weatherimage from '@/assets/pictures/weather.png';
import buildingtemp from '@/assets/pictures/building-temp.png';
import sensortemp from '@/assets/pictures/sensor-temp.png';
import email from '@/assets/pictures/email.png';
import timer from '@/assets/pictures/time.png';

const showCards1 = ref(false);
const showCards2 = ref(false);
const modalTriggerRef = ref(null);
const modalActionRef = ref(null);

// Selected service and trigger
const selectedService = ref('');
const selectedTrigger = ref('');
const selectedAction = ref('');

function toggleIfCards() {
    showCards1.value = !showCards1.value;
}

function toggleThenCards() {
    showCards2.value = !showCards2.value;
}

function openModal(title, type) {
    if (type === 'if') {
        modalTriggerRef.value?.openModal(title);
    } else if (type === 'then') {
        modalActionRef.value?.openModal(title);
    }
}

// Handle event from modal
function handleTriggerSelection({ service, trigger }) {
    selectedService.value = service;
    selectedTrigger.value = trigger;
}

function handleActionSelection({ action }) {
    selectedAction.value = action;
}
</script>

<template>
    <div class="main-wrapper">
        <div class="main-div-card">
            <div class="content">
                <h5 class="mb-4">Create</h5>
                <div class="ifthan-wrapper">
                    <div class="ifthan-div">
                        <div class="ifthan-header">
                            <div class="ifthan-header-card">
                                <span>If This</span>
                                <div class="d-flex">
                                    <div class="px-2">
                                        <a href="#" @click.prevent="toggleIfCards">
                                            <img :src="add">
                                        </a>
                                    </div>
                                    <div class="px-2">
                                        <a href="#"><img :src="edit"></a>
                                    </div>
                                    <div class="px-2">
                                        <a href="#"><img :src="del"></a>
                                    </div>
                                </div>
                            </div>
                            <hr>

                            <div v-if="selectedService && selectedTrigger" class="selected-servce">
                                <span><span class="fw-bold">Service: </span>{{ selectedService }}</span>
                                <span><span class="fw-bold">Rule: </span>{{ selectedTrigger }}</span>
                            </div>
                        </div>
                        <div class="ifthan-cards-div" v-if="showCards1">
                            <a href="#" class="ifthan-card" @click.prevent="openModal('Temperature', 'if')">
                                <img :src="weatherimage" class="weather-img">
                                <span>Weather</span>
                            </a>
                            <!-- <a href="#" class="ifthan-card" @click.prevent="openModal('Building Automation', 'if')">
                                <img :src="buildingtemp" class="weather-img">
                                <span>Building Automation</span>
                            </a> -->
                            <a href="#" class="ifthan-card" @click.prevent="openModal('Sensor Temperature', 'if')">
                                <img :src="sensortemp" class="weather-img">
                                <span>Temperature</span>
                            </a>
                            <!-- <a href="#" class="ifthan-card" @click.prevent="openModal('Email', 'if')">
                                <img :src="email" class="weather-img">
                                <span>Email</span>
                            </a> -->
                            <a href="#" class="ifthan-card" @click.prevent="openModal('Timer', 'if')">
                                <img :src="timer" class="weather-img">
                                <span>Timer</span>
                            </a>
                        </div>
                    </div>

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
                                        <a href="#" @click.prevent="toggleThenCards">
                                            <img :src="add">
                                        </a>
                                    </div>
                                    <div class="px-2">
                                        <a href="#"><img :src="edit"></a>
                                    </div>
                                    <div class="px-2">
                                        <a href="#"><img :src="del"></a>
                                    </div>
                                </div>
                            </div>
                            <hr>
                            <div class="selected-servce">
                                <span><span class="fw-bold">Service: </span>Weather</span>
                                <span><span class="fw-bold">Action: </span>Do this</span>
                            </div>
                        </div>
                        <div class="ifthan-cards-div" v-if="showCards2">
                            <!-- <a href="#" class="ifthan-card" @click.prevent="openModal('Temperature', 'then')">
                                <img :src="weatherimage" class="weather-img">
                                <span>Weather</span>
                            </a> -->
                            <a href="#" class="ifthan-card" @click.prevent="openModal('Building Automation', 'then')">
                                <img :src="buildingtemp" class="weather-img">
                                <span>Building Automation</span>
                            </a>
                            <!-- <a href="#" class="ifthan-card" @click.prevent="openModal('Sensor Temperature', 'then')">
                                <img :src="sensortemp" class="weather-img">
                                <span>Temperature</span>
                            </a> -->
                            <a href="#" class="ifthan-card" @click.prevent="openModal('Email', 'then')">
                                <img :src="email" class="weather-img">
                                <span>Email</span>
                            </a>
                            <!-- <a href="#" class="ifthan-card" @click.prevent="openModal('Timer', 'then')">
                                <img :src="timer" class="weather-img">
                                <span>Timer</span>
                            </a> -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <ModalTrigger ref="modalTriggerRef" @trigger-selected="handleTriggerSelection" />
    <ModalAction ref="modalActionRef" @action-selected="handleActionSelection" />
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