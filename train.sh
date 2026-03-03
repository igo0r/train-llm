#!/bin/bash
# Train Qwen2.5-Coder-7B with MLX LoRA

set -e

echo "======================================================================"
echo "Training Qwen2.5-Coder-7B with MLX LoRA"
echo "======================================================================"

MODEL="Qwen/Qwen2.5-Coder-7B"
DATA="/Users/igorlantushenko/train-llm/training_data/mlx_data"
ADAPTER_PATH="/Users/igorlantushenko/train-llm/adapters"
ITERS=1000

echo "Model: $MODEL"
echo "Data: $DATA"
echo "Adapters: $ADAPTER_PATH"
echo "Iterations: $ITERS"
echo ""

arch -arm64 /usr/local/bin/python3 -m mlx_lm lora \
    --model "$MODEL" \
    --train \
    --data "$DATA" \
    --adapter-path "$ADAPTER_PATH" \
    --batch-size 1 \
    --learning-rate 1e-5 \
    --iters $ITERS \
    --save-every 100 \
    --steps-per-report 10 \
    --fine-tune-type lora

echo ""
echo "Training complete!"
