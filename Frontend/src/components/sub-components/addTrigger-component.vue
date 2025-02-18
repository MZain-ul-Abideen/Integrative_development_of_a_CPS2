<template>
  <div class="add-trigger-wrapper">
    <!-- Conditional Rendering Based on Selected Service -->
    <WeatherRule v-if="selectedService === 'Temperature'" />
    <TemperatureRule v-if="selectedService === 'Sensor Temperature'" />
    <TimerRule v-if="selectedService === 'Timer'" />
  </div>
</template>

<script setup>
import WeatherRule from '@/components/sub-components/rule-modal/weather/weather-service.vue';
import TemperatureRule from '@/components/sub-components/rule-modal/Temperature/temperature-service.vue' ;
import TimerRule from '@/components/sub-components/rule-modal/Timer/timer-service.vue';

// Define Props
const props = defineProps({
  selectedService: {
    type: String,
    default: ''
  },
  selectedTrigger: {
    type: String,
    default: ''
  }
});
</script>

<style scoped>
.add-trigger-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}
</style>