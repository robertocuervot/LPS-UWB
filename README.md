# LPS-UWB

## Overview

This repository contains the development of a Local Positioning System (LPS) based on Ultra-Wideband (UWB) technology. The project's objective was to track the real-time positions of a volleyball team on the court. While the complete implementation was beyond the project's scope, preliminary tests were conducted to evaluate the accuracy and precision of the UWB modules, along with basic real-world trials of the prototype system.

The latest version of the project includes a working 2D positioning system using four fixed anchors and one mobile tag. The tag sends distance measurements via Wi-Fi (TCP) to a computer, where the data is processed and visualized in real time.

## Technology

The following hardware components were used in the development:

* M5 Atom Matrix – a microcontroller powered by an ESP32: https://shop.m5stack.com/products/atom-matrix-esp32-development-kit?srsltid=AfmBOor0EH-e7t1_7oSsxUbWGi5oRz10mO0Ssxk5bBYd5GEaz8sRuRpT

* M5 UWB module – based on Decawave's DW1000 chip: https://shop.m5stack.com/products/ultra-wideband-uwb-unit-indoor-positioning-module-dw1000?srsltid=AfmBOor4eKq1a_jDpYj-SxLlVuJqjyvXTqNVR3P4PVKOZdyS0G2HnHD0

## Repository Structure

More information can be found within each folder:

* M5AtomMatrix -> Arduino scripts for programming the M5 Atom Matrix and UWB module

* Scripts -> Python scripts for data processing and visualization

* Unity -> Unity project for 3D visualization (currently under development)

* Docs -> Complete project report (in French).