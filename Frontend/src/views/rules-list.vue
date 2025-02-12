<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

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

// Dropdown logic
const openDropdowns = ref(new Set());

function toggleDataTableMenuDropdown(index) {
  if (openDropdowns.value.has(index)) {
    openDropdowns.value.delete(index);
  } else {
    openDropdowns.value.clear(); // Ensure only one dropdown is open at a time
    openDropdowns.value.add(index);
  }
}

// Function to close dropdowns when clicking outside
function handleClickOutside(event) {
  // Check if the click target is outside any dropdowns or cards
  const dropdownElements = document.querySelectorAll(".data-table-menu-dropdown");
  let isClickInside = false;

  dropdownElements.forEach((dropdown) => {
    if (dropdown.contains(event.target)) {
      isClickInside = true;
    }
  });

  // If the click is outside, clear the open dropdowns
  if (!isClickInside) {
    openDropdowns.value.clear();
  }
}

// Add and remove event listeners for document click
onMounted(() => {
  document.addEventListener("mousedown", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("mousedown", handleClickOutside);
});

function dataTableMenuViewAction(id) {
  console.log(`View action triggered for ID: ${id}`);
  // Add your view logic here
}

function dataTableMenuDeleteAction(id) {
  console.log(`Delete action triggered for ID: ${id}`);
  // Add your delete logic here
}

const notifications = ref([
  {
    name: "Countdown",
    rule: "Rule 1",
    message: "Action 1",
    time: "10:00 AM",
    status: "Active",
  },
  {
    name: "High Temp",
    rule: "Rule 2",
    message: "Action 2",
    time: "11:00 AM",
    status: "Active",
  },
  {
    name: "Threshold",
    rule: "Rule 3",
    message: "Action 3",
    time: "12:00 PM",
    status: "Not Active",
  },
]);

</script>


<template>
    <div class="main-wrapper">
      <div
        class="main-div-card"
        @mousemove="handleMouseMove"
        @mouseleave="handleMouseLeave"
      >
        <div class="affect-global-blue1"></div>
        <div class="affect-global-blue2"></div>
        <div class="affect-global-blue3"></div>
        <div class="affect-global-yellow1"></div>
        <div class="affect-global-yellow2"></div>
        <div class="affect-global-lightblue1"></div>
        <div class="hover-effect"></div>
        <div class="content">
          <h5 class="mb-4">All Triggers</h5>
          <table>
            <thead>
              <tr>
                <th>Trigger Name</th>
                <th>Rule Service</th>
                <th>Action Service</th>
                <th>Time Created</th>
                <th>Status</th>
                <th class="action-column">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(notification, index) in notifications" :key="index">
                <td>{{ notification.name }}</td>
                <td>{{ notification.rule }}</td>
                <td>{{ notification.message }}</td>
                <td>{{ notification.time }}</td>
                <td>{{ notification.status }}</td>
                <td>
                  <div class="data-table-menu-dropdown">
                    <a
                      class="data-table-menu-button"
                      @click.stop="toggleDataTableMenuDropdown(index)"
                    >
                      ⋮
                    </a>
                    <div
                      v-if="openDropdowns.has(index)"
                      class="data-table-menu-dropdown-menu"
                    >
                      <a @click.prevent="dataTableMenuViewAction(notification.id)">View</a>
                      <a @click.prevent="dataTableMenuDeleteAction(notification.id)">Delete</a>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="my-4 d-flex justify-content-end">
            <nav aria-label="Page navigation example" class="pagination-div">
              <ul class="pagination">
                <li class="page-item">
                  <a class="page-link" href="#" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                    <span class="sr-only">Previous</span>
                  </a>
                </li>
                <li class="page-item"><a class="page-link" href="#">1</a></li>
                <li class="page-item"><a class="page-link" href="#">2</a></li>
                <li class="page-item"><a class="page-link" href="#">3</a></li>
                <li class="page-item">
                  <a class="page-link" href="#" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                    <span class="sr-only">Next</span>
                  </a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </template>
  

<style scoped>
.content {
    width: 100%;
    padding: 2rem;
}

table {
    width: 100%;
    border-collapse: collapse;
    overflow: hidden;
    border-radius: 3px;
}

thead th {
    text-align: left;
    padding: 15px;
    color: #fff;
    font-weight: bold;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-size: 1.3rem;
}

tbody td {
    padding: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

tbody tr:hover {
    background-color: rgba(255, 255, 255, 0.2);
    transition: background-color 0.3s ease;
}

.action-column {
    max-width: 3rem;
}
.page-link {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: var(--ui-1);
}

.data-table-menu-dropdown {
  position: relative;
  display: flex;
  justify-content: center;
}

.data-table-menu-button {
  cursor: pointer;
  font-size: 1.5rem;
  user-select: none;
  color: var(--ui-1);
  text-decoration: none;
}

.data-table-menu-dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: var(--ui-1);
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  width: 120px;
}

.data-table-menu-dropdown-menu a {
  display: block;
  padding: 0.5rem 1rem;
  color: var(--ui-2);
  text-decoration: none;
}

.data-table-menu-dropdown-menu a:hover {
    background-color: rgba(150, 150, 150, 0.479);
    color: var(--ui-2);
}
</style>