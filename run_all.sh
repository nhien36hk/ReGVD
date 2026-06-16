#!/bin/bash

# Resolve script directory and change to code directory
cd "$(dirname "$0")/code" || exit 1

# 1. Run Devign
echo "=================================================="
echo "Starting training on Devign dataset..."
echo "=================================================="
python3 -u run_reproduction.py --dataset devign_split --seed 123456 --batch_size 128 > ../devign_reproduce.log 2>&1

# 2. Run Reveal
echo "=================================================="
echo "Starting training on Reveal dataset..."
echo "=================================================="
python3 -u run_reproduction.py --dataset reveal_split --seed 123456 --batch_size 128 > ../reveal_reproduce.log 2>&1

