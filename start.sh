#!/bin/bash
echo "=== D3V4ST4T0R v5.0 ==="
echo "Target: $TARGET:$PORT"
echo "Tasks: $THREADS | Duration: ${DURATION}s"
echo ""

python3 flood.py
