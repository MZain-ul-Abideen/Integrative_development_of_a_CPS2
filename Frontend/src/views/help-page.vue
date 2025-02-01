<script setup>
import { ref } from 'vue';

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
}


// Store the currently opened FAQ index
const activeFAQ = ref(null);

// Function to toggle an FAQ
function toggleFAQ(index) {
    activeFAQ.value = activeFAQ.value === index ? null : index;
}

const faqs = [
    {
        question: "1. How do I create a rule?",
        answer: `To create a rule:<ul>
        <li>Navigate to the "Manager" section.</li>
        <li>Click on "Add Rule."</li>
        <li>Select a trigger (e.g., indoor temperature > 25°C).</li>
        <li>Define an action (e.g., send an email).</li>
        <li>Save the rule.</li>
        </ul>`
    },
    {
        question: "2. How do I integrate a new weather API?",
        answer: `To integrate a new weather API:<ul>
        <li>Go to the "Settings" section.</li>
        <li>Locate the "Weather API" section.</li>
        <li>Enter the provided API key and save the changes.</li>
        </ul>`
    },
    {
        question: "3. Why am I not receiving notifications?",
        answer: `If you're not receiving notifications:<ul>
        <li>Ensure that your preferred notification method is enabled in the "Notifications" section.</li>
        <li>Double-check your email or SMS settings to confirm they are correctly configured.</li>
        </ul>`
    },
    {
        question: "4. What should I do if sensor data is not updating?",
        answer: `If sensor data is not updating:<ul>
        <li>Confirm that the sensors are powered on and properly connected.</li>
        <li>Check the MQTT settings to ensure everything is configured correctly.</li>
        </ul>`
    },
    {
        question: "5. How do I troubleshoot API errors?",
        answer: `To resolve API errors:<ul>
        <li>Verify that your API keys are entered correctly in the "Settings" section.</li>
        <li>Check the system logs in "Settings" for additional details about the error.</li>
        </ul>`
    },
    {
        question: "6. Why are my rules not triggering?",
        answer: `If your rules are not triggering:<ul>
        <li>Verify that the triggers and conditions in your rule are active and properly configured.</li>
        <li>Check the failure logs for details on why the rule might not have executed.</li>
        </ul>`
    },
    {
        question: "7. What are some tips for optimizing the system?",
        answer: `<ul>
        <li>Regularly review and update your automation rules to ensure they are efficient and relevant.</li>
        <li>Use the "Notifications" history to analyze trends and identify potential system improvements.</li>
        <li>Keep your API keys up-to-date to prevent interruptions in service.</li>
        </ul>`
    },
    {
        question: "8. How can I view system performance and real-time data?",
        answer: `You can view system performance, real-time data, and alerts on the "Dashboard" section of the platform.`
    },
    {
        question: "9. How do I customize MQTT and API configurations?",
        answer: `To customize MQTT and API settings:<ul>
        <li>Go to the "Settings" section.</li>
        <li>Adjust the configurations according to your system requirements.</li>
        </ul>`
    },
    {
        question: "10. What should I do to analyze notification trends?",
        answer: `Use the "Notifications" history section to review past alerts and analyze system performance trends.`
    },
];
</script>
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
                <h5>Help Center</h5>
                <p>Everything you need to know about this product!</p>
                <hr>
                <div class="row">
                    <div class="col-3">
                        <p>Support</p>
                        <h4>FAQs</h4>
                        <span>Everything you need to know about this product. Can't find the answer you're looking for?
                            Please <a href="" class="text-light">chat with the team.</a></span>
                    </div>
                    <div class="col-9">
                        <div class="faq-wrapper">
                            <div v-for="(faq, index) in faqs" :key="index" class="faq-item">
                                <!-- FAQ Question -->
                                <div class="faq-question" @click="toggleFAQ(index)">
                                    {{ faq.question }}
                                    <span class="arrow" :class="{ open: activeFAQ === index }">▼</span>
                                </div>

                                <!-- FAQ Answer (Collapsible) -->
                                <div v-show="activeFAQ === index" class="faq-answer">
                                    <p v-html="faq.answer"></p>
                                </div>
                            </div>
                        </div>
                    </div>
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

.faq-wrapper {
    width: 100%;
}

.faq-question {
    font-weight: bold;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem;
    border-radius: 5px;
    transition: background 0.3s ease;
}

.faq-question:hover {
    background: #f1f1f11c;
}

.arrow {
    transition: transform 0.3s ease;
}

.arrow.open {
    transform: rotate(180deg);
}

.faq-answer {
    padding: 1rem;
    font-size: 1rem;
    color: var(--ui-1);
    animation: slideDown 0.3s ease;
}

@keyframes slideDown {
    from {
        opacity: 0;
        max-height: 0;
    }

    to {
        opacity: 1;
        max-height: 100px;
    }
}
</style>