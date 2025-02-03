<template>
    <div class="add-trigger-wrapper">
      <!-- Conditional Rendering Based on Selected Service -->
      <EmailAction v-if="selectedService === 'Email'" />
      <AutomationAction v-if="selectedService === 'Building Automation'" />
    </div>
  </template>
  
  <script setup>
  import EmailAction from '@/components/sub-components/action-modal/Email/email-service.vue';
  import AutomationAction from '@/components/sub-components/action-modal/Automation/automation-service.vue' ;
  
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