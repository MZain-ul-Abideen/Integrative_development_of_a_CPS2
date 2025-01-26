<script setup>
// Define the functions directly in the setup block
function handleMouseMove(event) {
    const card = event.currentTarget;
    const hoverEffect = card.querySelector('.hover-effect');

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
    const hoverEffect = event.currentTarget.querySelector('.hover-effect');
    hoverEffect.style.opacity = 0; // Hide the shadow on mouse leave
}</script>
<template>
    <div class="main-wrapper">
        <div class="main-div-card" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave">
            <div class="affect-global-blue1"></div>
            <div class="affect-global-blue2"></div>
            <div class="affect-global-blue3"></div>
            <div class="affect-global-yellow1"></div>
            <div class="affect-global-yellow2"></div>
            <div class="affect-global-lightblue1"></div>
            <div class="hover-effect"></div>
            <div class="content">
                <h5 class="mb-4">Notifications</h5>
                <table>
                    <thead>
                        <th>Time</th>
                        <th>Triggered Rule</th>
                        <th>Message</th>
                        <th>Type</th>
                        <th>Status</th>
                        <th class="action-column">Actions</th>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                        </tr>
                        <tr>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                        </tr>
                        <tr>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                            <td>Lorem</td>
                        </tr>
                    </tbody>
                </table>
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
            max-width: 10px;
        }
        </style>