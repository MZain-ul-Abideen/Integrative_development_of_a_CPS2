<script setup>
import logo from '@/assets/logos/logo4.png';
import dashboard from '@/assets/svgs/dashboard.svg';
import service from '@/assets/svgs/service.svg';
import notifications from '@/assets/svgs/notifications.svg';
import settings from '@/assets/svgs/settings.svg';
import help from '@/assets/svgs/help.svg';
</script>

<template>
    <div class="main-div flex-column">
        <div class="nav-div">
            <img :src="logo" alt="Logo" class="logo-image">
            <div class="wraper-div mt-5">
                <div class="nav-btn py-2 my-4">
                    <router-link to="/create" class="svg-image my-1">
                        <img :src="service" alt="Logo" >
                    </router-link>
                </div>
                <div class="nav-btn py-2 my-4">
                    <router-link to="/rules" class="svg-image my-1">
                        <img :src="notifications" alt="Logo" >
                    </router-link>
                </div>
            </div>
            <div class="affect-1"></div>
        </div>
    </div>
</template>

<style scoped>
.main-div {
    background-color: var(--card-1); /* Semi-transparent white */
    backdrop-filter: blur(10px); /* Apply blur for glass effect */
    -webkit-backdrop-filter: blur(10px); /* For Safari */
    border-radius: 1.5rem; /* Optional: Rounded corners for a smooth look */
    height: 100%;
    width: 100%;
    padding-top: 2em;
}

.nav-div {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.logo-image {
    width: 100%;
    height: auto;
}

.svg-image {
    width: 100%;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
}

.svg-image:hover {
    background-color: var(--card-2); /* Semi-transparent white */
    border-radius: 1rem; /* Optional: Rounded corners for a smooth look */
    transition: 0.3s;
}

.help-icon {
    position: absolute; /* Position relative to the container */
    bottom: 0;
    cursor: pointer;
}

.wraper-div {
    width: 100%;
}

.nav-btn {
    position: relative; /* Position relative to handle the pseudo-element */
    transition: background 0.9s ease-in-out; /* Smooth background change */
    background: transparent; /* Initial background */
    cursor: pointer;
}

.nav-btn:hover {
    background: linear-gradient(90deg, rgb(168, 168, 168) 0%, rgba(136,136,136,0.45) 100%);
    transition: transform 0.3s ease-in-out; /* Smooth expand animation */

}

/* Add the bar effect */
.nav-btn::before {
    content: '';
    position: absolute;
    top: 50%; /* Center vertically */
    left: 0; /* Start from the left */
    transform: translateY(-50%) scaleX(0); /* Initially hidden */
    width: 4px; /* Width of the bar */
    height: 100%; /* Height of the bar */
    background-color: rgb(255, 255, 255); /* Use your primary color */
    transition: transform 0.3s ease-in-out; /* Smooth expand animation */
    transform-origin: left; /* Expand from the left */
}

.nav-btn:hover::before {
    transform: translateY(-50%) scaleX(1); /* Expand the bar */
}

.affect-1 {
    height: 100px;
    width: 100%;
    background: linear-gradient(0deg, rgba(62,205,224,0.20772058823529416) 0%, rgba(192,239,245,0.11808473389355745) 100%);
    position: absolute;
    bottom: 100px;
    z-index: -1;
    opacity: 0.9; /* Slightly higher transparency for feathered look */
    pointer-events: none; /* Prevent interaction */
    filter: blur(35px); /* Apply blur to create a feathered edge */
    border-radius: 50%;
}


</style>