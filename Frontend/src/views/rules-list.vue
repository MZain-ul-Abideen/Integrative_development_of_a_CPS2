<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import axios from "axios"; // Import Axios for making HTTP requests

// Reactive variables
const notifications = ref([]); // Stores the linked rules and actions
const openDropdowns = ref(new Set()); // Tracks open dropdowns

// Event listeners for hover effects
function handleMouseMove(event) {
  const card = event.currentTarget;
  const hoverEffect = card.querySelector(".hover-effect");
  const rect = card.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  hoverEffect.style.top = `${y - 100}px`;
  hoverEffect.style.left = `${x - 100}px`;
  hoverEffect.style.opacity = 1;
}
function handleMouseLeave(event) {
  const hoverEffect = event.currentTarget.querySelector(".hover-effect");
  hoverEffect.style.opacity = 0;
}

// Dropdown logic
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
  const dropdownElements = document.querySelectorAll(".data-table-menu-dropdown");
  let isClickInside = false;
  dropdownElements.forEach((dropdown) => {
    if (dropdown.contains(event.target)) {
      isClickInside = true;
    }
  });
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

// Fetch linked rules and actions from the API
async function fetchLinkedRulesActions() {
  try {
    const response = await axios.get("http://127.0.0.1:5000/linked-rules-actions");
    // Debugging: Log the raw API response
    console.log("API Response:", response.data);
    // Map the API response to match the table structure
    notifications.value = response.data.map(link => ({
      ID: link.rule_id,
      Trigger: `${link.rule_service.name} - ${link.rule_name} (${link.rule_condition})`,
      Action: `${link.action_service.name} - ${link.action_name}`,
      rule_id: link.rule_id, // Add rule_id for deletion
      action_id: link.action_id // Add action_id for deletion
    }));
    // Debugging: Log the mapped notifications
    console.log("Mapped Notifications:", notifications.value);
  } catch (error) {
    console.error("Error fetching linked rules and actions:", error);
    // Handle errors
    if (error.response) {
      console.error("Server Response:", error.response.data);
      alert(`Error fetching linked rules and actions: ${error.response.data.error || error.response.statusText}`);
    } else {
      alert("An unexpected error occurred while fetching linked rules and actions.");
    }
  }
}

// Actions for dropdown menu
function dataTableMenuViewAction(id) {
  console.log(`View action triggered for ID: ${id}`);
  // Add your view logic here
}

// Delete action for unlinking rule and action
async function dataTableMenuDeleteAction(notification) {
  try {
    const confirmDelete = window.confirm(
      `Are you sure you want to unlink Rule ID: ${notification.rule_id} and Action ID: ${notification.action_id}?`
    );
    if (!confirmDelete) return;

    // Send DELETE request to unlink rule and action
    const response = await axios.delete(
      `http://127.0.0.1:5000/unlink-rule-action/${notification.rule_id}/${notification.action_id}`
    );

    // Check if the unlink was successful
    if (response.status === 200) {
      alert("Rule and action unlinked successfully.");
      // Refresh the notifications list after deletion
      fetchLinkedRulesActions();
    } else {
      alert("Failed to unlink rule and action.");
    }
  } catch (error) {
    console.error("Error unlinking rule and action:", error);
    if (error.response) {
      alert(`Error unlinking rule and action: ${error.response.data.error || error.response.statusText}`);
    } else {
      alert("An unexpected error occurred while unlinking rule and action.");
    }
  }
}

// Call fetchLinkedRulesActions when the component is mounted
onMounted(fetchLinkedRulesActions);
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

      <!-- Content -->
      <div class="content">
        <h5 class="mb-4">Rules List</h5>
        <table>
          <thead>
            <tr>
              <th>Rule ID</th>
              <th>Trigger Name</th>
              <th>Action Name</th>
              <th class="action-column text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(notification, index) in notifications" :key="index">
              <td>{{ notification.ID }}</td>
              <td>{{ notification.Trigger }}</td>
              <td>{{ notification.Action }}</td>
              <td>
                <!-- Dropdown menu -->
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
                    <a
                      href="#"
                      @click.prevent="dataTableMenuDeleteAction(notification)"
                    >
                      Delete
                    </a>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
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
  cursor: pointer;
}

.data-table-menu-dropdown-menu a:hover {
  background-color: rgba(150, 150, 150, 0.479);
  color: var(--ui-2);
}
</style>