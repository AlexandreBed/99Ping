#!/bin/bash

echo "Hello, I ran at startup!" >> /home/pi/startup.log

echo pcf8574 0x38 | sudo tee /sys/bus/i2c/devices/i2c-10/new_device
echo pcf8574 0x39 | sudo tee /sys/bus/i2c/devices/i2c-10/new_device

echo "Les PCF8574a exist aux addr 0x38 et 0x39 sur le bus i2c10" >> /home/pi/startup.log
