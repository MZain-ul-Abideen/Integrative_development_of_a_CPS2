<script setup>
import weatherimage from '@/assets/pictures/weather.png';
import buildingtemp from '@/assets/pictures/building-temp.png';
import exclamation from '@/assets/svgs/exclamation.svg';
import location from '@/assets/svgs/location.svg';
import date from '@/assets/svgs/date.svg';
import weeklyweather from '@/assets/pictures/weekly-weather.png';
import sun from '@/assets/pictures/sun.png';
import notifications from '@/assets/svgs/notifications2.svg';
import humidityimage from '@/assets/pictures/humidity.png';

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

const weeklyWeather = [
  { name: 'Sun', icon: weeklyweather, temp: 28 },
  { name: 'Mon', icon: weeklyweather, temp: 24 },
  { name: 'Tue', icon: weeklyweather, temp: 30 },
  { name: 'Wed', icon: weeklyweather, temp: 25 },
  { name: 'Thu', icon: weeklyweather, temp: 27 },
  { name: 'Fri', icon: weeklyweather, temp: 22 },
  { name: 'Sat', icon: weeklyweather, temp: 29 },
];
</script>


<template>
  <section class="dashboard-wrapper">
    <div class="d-flex flex-column dashboard-div">
      <!-- Row 1 -->
      <div class="card-div pb-2">
        <div class="col-4 mini-card-div">
          <div class="transperent-card" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave">
            <div class="hover-effect"></div>
            <div class="affect-mini-card-blue-1"></div>
            <div class="affect-mini-card-blue-2"></div>
            <div class="affect-mini-card-yellow"></div>
            <div class="d-flex justify-content-end p-4 info-icon">
              <img :src="exclamation" title="Outside city temperature!">
            </div>
            <div class="weather-data">
              <img :src="weatherimage" class="weather-img">
              <h3 class="mt-3">28°C</h3>
              <p>High: 32 Low: 22</p>
            </div>
            <div class="card-bottom">
              <hr>
              <div class="d-flex justify-content-between my-4 px-4">
                <span class="d-flex align-items-center">
                  <img :src="location" class="mx-2">
                  Saint Etienne: France
                </span>
                <span class="d-flex align-items-center">
                  <img :src="date" class="mx-2">
                  26 Jan, 2025
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-8 max-card-div">
          <div class="transperent-card" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave">
            <div class="max-card-affect1"></div>
            <div class="max-card-affect2"></div>
            <div class="max-card-affect3"></div>
            <div class="hover-effect"></div>
            <div class="px-5 pt-2 d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center">
                <img :src="sun" alt="">
                <div>
                  <h4>This Week</h4>
                  <span>Mostly Sunny</span>
                </div>
              </div>
              <div class="temp-avg">
                <h3>28°C</h3>
                <span>42°C/12°C</span>
              </div>
            </div>
            <div class="weekly-weather">
              <div v-for="(day, index) in weeklyWeather" :key="index" class="day-card">
                <h5>{{ day.name }}</h5>
                <img :src="day.icon" alt="weather icon" class="weather-icon">
                <p>{{ day.temp }}°C</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Row 2 -->
      <div class="card-div pt-2">
        <div class="col-4 mini-card-div">
          <div class="transperent-card" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave">
            <div class="hover-effect"></div>
            <div class="affect-mini-card-blue-1"></div>
            <div class="affect-mini-card-blue-2"></div>
            <div class="affect-mini-card-yellow"></div>
            <div class="d-flex justify-content-end p-4 info-icon">
              <img :src="exclamation" title="Room temperature!">
            </div>
            <div class="weather-data">
              <img :src="buildingtemp" class="buildingtemp-img">
              <h3 class="mt-3">28°C</h3>
              <p>High: 32 Low: 22</p>
            </div>
            <div class="card-bottom">
              <hr>
              <div class="d-flex justify-content-between my-4 px-4">
                <span class="d-flex align-items-center">
                  <img :src="location" class="mx-2">
                  Room G123
                </span>
                <span class="d-flex align-items-center">
                  <img :src="date" class="mx-2">
                  26 Jan, 2025
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-4 mini-card-div">
          <div class="transperent-card" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave">
            <div class="hover-effect"></div>
            <div class="affect-mini-card-blue-1"></div>
            <div class="affect-mini-card-blue-2"></div>
            <div class="affect-mini-card-yellow"></div>
            <div class="d-flex justify-content-end p-4 info-icon">
              <img :src="exclamation" title="Outside city temperature!">
            </div>
            <div class="weather-data">
              <img :src="humidityimage" class="weather-img">
              <h3 class="mt-3">80%</h3>
              <p>The Due Point is 27° right now</p>
            </div>
            <div class="card-bottom">
              <hr>
              <div class="d-flex justify-content-between my-4 px-4">
                <span class="d-flex align-items-center">
                  <img :src="location" class="mx-2">
                  Saint Etienne: France
                </span>
                <span class="d-flex align-items-center">
                  <img :src="date" class="mx-2">
                  26 Jan, 2025
                </span>
              </div>

            </div>
          </div>
        </div>
        <div class="d-flex flex-row col-4 mini-card-div p-0">
          <div class="transperent-card" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave">
            <div class="hover-effect"></div>
            <div class="affect-mini-card-blue"></div>
            <div class="notification-list px-4 pt-4">
              <span>Notifications</span>
              <div class="notification-list-item d-flex my-3">
                <img :src="notifications">
                <div class="mx-4">
                  <h5 class="m-0">The Alerts show here!</h5>
                  <span>15H34 - 13 jan 2025</span>
                </div>
              </div>
              <div class="notification-list-item d-flex my-3">
                <img :src="notifications">
                <div class="mx-4">
                  <h5 class="m-0">The Alert</h5>
                  <span>15H34 - 13 jan 2025</span>
                </div>
              </div>
              <div class="notification-list-item d-flex my-3">
                <img :src="notifications">
                <div class="mx-4">
                  <h5 class="m-0">The Alert Lorem ipsum dolor sit amet.</h5>
                  <span>15H34 - 13 jan 2025</span>
                </div>
              </div>
              <div class="notification-list-item d-flex my-3">
                <img :src="notifications">
                <div class="mx-4">
                  <h5 class="m-0">Lorem, ipsum dolor sit amet consectetur adipisicing elit. Doloribus magnam adipisci
                    corrupti minima nesciunt, dolore explicabo ipsam, quaerat molestias tenetur tempora debitis suscipit
                    sapiente quasi nemo, earum voluptas aspernatur odio.</h5>
                  <span>15H34 - 13 jan 2025</span>
                </div>
              </div>
              <div class="notification-list-item d-flex my-3">
                <img :src="notifications">
                <div class="mx-4">
                  <h5 class="m-0">Dolore, enim aliquid quae molestias praesentium.</h5>
                  <span>15H34 - 13 jan 2025</span>
                </div>
              </div>
            </div>
            <div class="view-all-div">
              <hr>
              <div class="view-all-btn">
                <router-link to="/notifications">View All</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.dashboard-wrapper {
  display: flex;
  flex-direction: row;
  height: 100%;
}

.dashboard-div {
  width: 100%;
}

.card-div {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 50%;
}

.mini-card-div {
  height: 100%;
  /* Adjust height as needed */
  display: flex;
  justify-content: center;
  align-items: center;
  padding-right: 20px;
}

.max-card-div {
  height: 100%;
  /* Adjust height as needed */
  display: flex;
  justify-content: center;
  align-items: center;
}


.transperent-card {
  height: 100%;
  width: 100%;
  border-radius: 30px;
  background-color: var(--card-1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  /* To contain the shadow within the card */
}

.affect-mini-card-blue-1 {
  height: 200px;
  width: 200px;
  background: linear-gradient(0deg, rgba(39, 140, 153, 0.788) 0%, rgba(36, 132, 145, 0.644) 100%);
  position: absolute;
  bottom: 100px;
  right: 100px;
  z-index: -1;
  opacity: 0.9;
  /* Slightly higher transparency for feathered look */
  pointer-events: none;
  /* Prevent interaction */
  filter: blur(100px);
  /* Apply blur to create a feathered edge */
  border-radius: 50%;
}

.affect-mini-card-blue-2 {
  height: 100px;
  width: 100px;
  background: linear-gradient(0deg, rgba(39, 140, 153, 0.788) 0%, rgba(36, 132, 145, 0.644) 100%);
  position: absolute;
  bottom: 100px;
  right: 300px;
  z-index: -1;
  opacity: 0.9;
  /* Slightly higher transparency for feathered look */
  pointer-events: none;
  /* Prevent interaction */
  filter: blur(70px);
  /* Apply blur to create a feathered edge */
  border-radius: 50%;
}

.affect-mini-card-yellow {

  height: 100px;
  width: 100px;
  background: #FFC62D;
  position: absolute;
  top: 100px;
  left: 100px;
  z-index: -1;
  opacity: 0.9;
  /* Slightly higher transparency for feathered look */
  pointer-events: none;
  /* Prevent interaction */
  filter: blur(75px);
  /* Apply blur to create a feathered edge */
  border-radius: 50%;
}

.info-icon img {
  cursor: pointer;
}

.weather-data {
  padding-left: 3rem;

}

.weekly-weather {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1rem;
  padding: 1rem;
  justify-items: center;
  align-items: center;
}

.day-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.8rem;
  width: 100%;
}

.day-card h5 {
  font-size: 1.9rem;
  margin: 0.5rem 0;
}

.day-card .weather-icon {
  height: 40px;
  margin: 0.5rem 0;
}

.temp-avg {
  display: flex;
  flex-direction: column;
  align-items: end;
}

.temp-avg span {
  font-size: 1.6rem;
  opacity: 0.7;
}

.max-card-affect1 {
  height: 100px;
  width: 100px;
  background: #FFC62D;
  position: absolute;
  top: 50px;
  left: 75px;
  z-index: -1;
  opacity: 0.9;
  /* Slightly higher transparency for feathered look */
  pointer-events: none;
  /* Prevent interaction */
  filter: blur(75px);
  /* Apply blur to create a feathered edge */
  border-radius: 50%;
}

.max-card-affect2 {
  height: 200px;
  width: 200px;
  background: #1D6FF2;
  position: absolute;
  top: 50px;
  right: 75px;
  z-index: -1;
  opacity: 0.9;
  /* Slightly higher transparency for feathered look */
  pointer-events: none;
  /* Prevent interaction */
  filter: blur(200px);
  /* Apply blur to create a feathered edge */
  border-radius: 50%;
}

.max-card-affect3 {
  height: 200px;
  width: 200px;
  background: #FFC62D;
  position: absolute;
  top: 150px;
  right: 350px;
  z-index: -1;
  opacity: 0.9;
  /* Slightly higher transparency for feathered look */
  pointer-events: none;
  /* Prevent interaction */
  filter: blur(200px);
  /* Apply blur to create a feathered edge */
  border-radius: 50%;
}

.notification-list-item h5 {
  font-size: 1.2rem;
  font-weight: 300;
  white-space: nowrap;
  /* Prevent text from wrapping to the next line */
  overflow: hidden;
  /* Hide overflow text */
  text-overflow: ellipsis;
  /* Add ellipsis for overflow text */
  max-width: 45ch;
  /* Limit to 100 characters */
}

.notification-list-item span {
  font-size: 0.9rem !important;
  opacity: 0.7;
  display: block;
  /* Make span behave as block-level */
  white-space: nowrap;
  /* Prevent text from wrapping */
  overflow: hidden;
  /* Hide overflow text */
  text-overflow: ellipsis;
  /* Add ellipsis for overflow text */
  max-width: 45ch;
  /* Limit to 100 characters */
}

.notification-list span {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--ui-1);
}

.view-all-div {
  position: absolute;
  bottom: 0;
  width: 100%;
}

.view-all-btn {
  text-align: center;
  margin: 1rem;
}

.view-all-btn a {
  color: var(--ui-1);
  text-decoration: none;
  transition: 0.3s;
}

.affect-mini-card-blue {
  height: 100px;
  width: 100px;
  background: #618ed6;
  position: absolute;
  top: 50px;
  right: 75px;
  z-index: -1;
  opacity: 0.9;
  /* Slightly higher transparency for feathered look */
  pointer-events: none;
  /* Prevent interaction */
  filter: blur(100px);
  /* Apply blur to create a feathered edge */
  border-radius: 50%;
}

.other-info-card {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--ui-1);
}

.card-bottom {
  position: absolute;
  bottom: 0;
  width: 100%;
}
</style>
