#!/bin/bash
sleep 5  # Wait for five seconds
echo "Running script at $(date)" >> /home/abba/Desktop/Applazen/script.log
sed -i '$ s/.$//' /home/abba/Desktop/Applazen/add.html >> /home/abba/Desktop/Applazen/script.log 2>&1
