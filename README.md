# FieldGuard — Distributed Agricultural IoT Monitoring

**Three zones. One watchful field.**

FieldGuard is a student-built AgriTech IoT prototype for distributed environmental monitoring using **ESP32, LoRa, and temperature/humidity sensors**.

The prototype was developed by **Team Alpha during IoT Summer Camp Bremen 2026**. The goal was to explore how multiple sensing zones can communicate environmental conditions over long-range wireless links to a central monitoring unit.

🌐 **Interactive Project Website:**  
https://aaushh2705.github.io/fieldguard-agritech-iot/
---

## 🌱 The Idea

Agricultural environments such as greenhouses, remote fields, barns, and storage areas may require environmental monitoring across locations where conventional Wi-Fi connectivity is impractical.

FieldGuard demonstrates a simple distributed architecture:

**3 Sensor Zones → ESP32 Processing → LoRa Transmission → Central Receiver → Alerts**

Each sensing zone monitors environmental conditions and communicates the information wirelessly to a receiver.

---

## ⚙️ Prototype Architecture

### Sensing
- 3 distributed monitoring zones
- DHT11 temperature and humidity sensors
- Zone identification and condition monitoring

### Processing
- ESP32 / MoleNet microcontrollers
- Local sensor acquisition
- Alert-state logic

### Communication
- SX127x LoRa transceiver
- **868 MHz**
- **125 kHz bandwidth**
- **Spreading Factor 9**
- CRC enabled

### Receiver
The central receiver processes incoming LoRa messages and provides feedback through:

- LCD display
- Status LED
- Buzzer alerts
- Zone-specific condition information

---

## 🚨 Monitoring Logic

The prototype classifies temperature conditions into three states:

| Temperature | State |
|---|---|
| `< 25°C` | NORMAL |
| `25–29°C` | WARNING |
| `≥ 30°C` | CRITICAL |

The receiver identifies which zone requires attention and updates the system status accordingly.

---

## 🧠 What We Explored

FieldGuard was primarily an exercise in **embedded systems and system integration**, rather than only sensor measurement.

The project involved:

- ESP32 sensor interfacing
- LoRa point-to-point communication
- Multi-zone message handling
- Wireless configuration and debugging
- Alert logic
- Hardware integration
- Receiver-side visualization
- Troubleshooting communication interference

---

## 🌾 Potential Applications

The same architecture could potentially be adapted for:

- Greenhouse environmental monitoring
- Remote agricultural fields
- Livestock and barn monitoring
- Agricultural storage monitoring

Additional sensors such as **soil moisture, light, rainfall, or gas sensors** could also be integrated in future versions.
Alongwith a cloud based notification system via Telegram (Toit programs will be used ) 'UNDER UPDATE'
> FieldGuard is a student engineering proof-of-concept and not a commercially deployed agricultural monitoring system.

---

## 💻 Interactive Web Demo

This repository also contains an interactive project website.

The browser-based demonstration allows visitors to change the simulated temperature of each zone and observe how FieldGuard's receiver responds to **NORMAL, WARNING, and CRITICAL** conditions.

The web interface is intended to explain the engineering concept visually and does not represent live sensor telemetry.

---

## 🛠️ Technology

`ESP32` · `LoRa` · `SX127x` · `DHT11` · `Embedded Systems` · `IoT` · `Wireless Communication` · `HTML` · `CSS` · `JavaScript`

---

## 📁 Repository Structure

```text
fieldguard-agritech-iot/
├── assets/
│   ├── images/
│   └── logos/
├── index.html
├── style.css
├── script.js
├── README.md
└── LICENSE
```

---

## 👥 Project Origin

**Team Alpha**  
IoT Summer Camp Bremen 2026

FieldGuard was developed as a student engineering prototype combining sensing, embedded processing, long-range wireless communication, and system-level monitoring.

---

## 📸 Prototype

Real prototype photographs, system setup images, and the project poster are available in the `assets/images` directory.

---

## 👤 Contributor

**Aayush Srivastava**  
M.Sc. Control, Microsystems and Microelectronics  
University of Bremen

Focus: **Robotics · Automation · Control Systems · Embedded/IoT · System Integration**

