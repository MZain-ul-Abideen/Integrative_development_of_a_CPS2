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
                <div class="main-div-content">
                    <h1>404</h1>
                    <h5>Page not found!</h5>
                    <p class="mb-4">Sorry we can't find the page you are looking for </p>
                    <div>
                        <router-link to="/dashboard" class="button-1">Go to Home</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.content {
    text-align: center;
    animation: fadeIn 1.5s ease-in-out;
    height: 100%;
}

.main-div-content {
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 90%;
}

h1 {
    font-size: 6rem;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.1);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}
</style>