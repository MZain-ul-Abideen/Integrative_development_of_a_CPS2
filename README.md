# **Integrative Development of CPS2: ESP32 with MicroPython**

## **Overview**
This repository is part of the **Integrative Development of CPS2** project. It involves using an **ESP32 microcontroller** with **MicroPython** to send temperature and humidity data from sensors to a backend system. Development is conducted in **Visual Studio Code** with the **pyMakr** extension.

---

## **Features**
- **Microcontroller**: ESP32
- **Development Environment**: VS Code with pyMakr
- **Sensors**:
  - **DHT22**: Temperature and humidity
  - **TEHT 6000**: Ambient light
- **Functionality**:
  - Collect sensor data
  - Send temperature and humidity data to the backend

---

## **Setup**

### **Hardware Setup**
1. Connect the DHT22 sensor to the ESP32:
   - **VCC** to **3.3V**
   - **GND** to **GND**
   - **Data Pin** to a digital pin (e.g., D21)
2. Connect the TEHT 6000 sensor:
   - **VCC** to **3.3V**
   - **GND** to **GND**
   - **Signal Pin** to an analog pin (e.g., A3)

### **Software Setup**
1. Install **Visual Studio Code** and the **pyMakr extension**.
2. Install Python 3.x and esptool:
   ```bash
   pip install esptool
   ```
3. Flash MicroPython firmware to ESP32:
   ```bash
   esptool.py --chip esp32 erase_flash
   esptool.py --chip esp32 --port <your_port> write_flash -z 0x1000 <firmware.bin>
   ```
4. Clone the repository:
   ```bash
   git clone https://gitlab.emse.fr/scrum/Ecole-des-mines.git
   ```
   When you clone the repo it has all fron end back end and embeded part. Go to embedded part.
5. Open the embedded part in VS Code and configure pyMakr.
6. Upload the code to ESP32 using pyMakr.

---


## **Contributing**
1. Fork the repo.
2. Create a feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit and push changes.
4. Open a merge request.

---

## **License**
Licensed under the **MIT License**.