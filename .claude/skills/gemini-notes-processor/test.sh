#!/bin/bash

echo "[$(date +%H:%M:%S)] gemini-notes-processor: starting"
echo "[$(date +%H:%M:%S)] invoking claude..."

claude -p "/gemini-notes-processor"

echo "[$(date +%H:%M:%S)] gemini-notes-processor: done"