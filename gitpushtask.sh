#!/bin/bash
sleep 5  # Wait for five seconds
echo "Running script at $(date)" >> /home/abba/Desktop/Applazen/script.log
cd
cd /home/abba/Desktop/Applazen
./git_push.sh >> /home/abba/Desktop/Applazen/script.log 2>&1
