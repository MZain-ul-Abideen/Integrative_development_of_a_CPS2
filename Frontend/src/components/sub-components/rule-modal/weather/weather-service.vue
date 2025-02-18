<template>
    <div class="add-trigger-div">
        <div class="nav-btn-wrapper">
          <button
        class="nav-btn"
        :class="{ active: activeTab === 'temperature' }"
        @click="activeTab = 'temperature'"
      >
        Temperature
      </button>

      <!-- Forecast Button -->
      <button
        class="nav-btn"
        :class="{ active: activeTab === 'forecast' }"
        @click="activeTab = 'forecast'"
      >
        Forecast
      </button>
        </div>
        <hr>
        <!-- Conditionally render components -->
        <WeatherComponent v-if="activeTab === 'temperature'" />
        <ForecastComponent v-if="activeTab === 'forecast'" />
      </div>    
</template>

<script setup>
import { ref } from 'vue';
  import WeatherComponent from '@/components/sub-components/rule-modal/weather/weather-component.vue';
  import ForecastComponent from '@/components/sub-components/rule-modal/weather/forecast-component.vue';

  const activeTab = ref('temperature'); // Default to Temperature
</script>

<style scoped>
.add-trigger-div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.nav-btn {
  background: transparent;
  color: var(--ui-1);
  border: none;
  margin-bottom: 1rem;
  font-size: 1.3rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.nav-btn.active {
  font-weight: bolder; /* Optional: Add bold text for active button */
}

.nav-btn:not(.active):hover {
  color: var(--ui-2); /* Hover color for inactive buttons */
}
.add-trigger-div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
}
.nav-btn-wrapper {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 2rem;
    border-bottom: 1px solid var(--ui-1);
    padding-left: 1rem;
    padding-right: 1rem;
}

</style>