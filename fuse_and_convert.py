import os
import subprocess
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from safetensors import safe_open

print("=" * 70)
print("FUSING ADAPTERS AND CONVERTING TO GGUF")
print("=" * 70)
print()

base_model = "Qwen/Qwen2.5-Coder-7B"
adapter_path = "/Users/igorlantushenko/train-llm/adapters"
output_dir = "/Users/igorlantushenko/train-llm/playdash-cool-fused"
output_gguf = "/Users/igorlantushenko/train-llm/playdash-cool.gguf"

print("Step 1: Loading base model...")
print(f"  Base: {base_model}")

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
base = AutoModelForCausalLM.from_pretrained(
    base_model, torch_dtype="auto", device_map="cpu", trust_remote_code=True
)

print("Step 2: Loading adapter weights...")
adapter_file = os.path.join(adapter_path, "adapters.safetensors")
adapter_weights = {}
with safe_open(adapter_file, framework="pt") as f:
    for key in f.keys():
        adapter_weights[key] = f.get_tensor(key)
print(f"  Loaded {len(adapter_weights)} adapter tensors")

print("Step 3: Applying adapters to model...")
lora_scale = 20.0


def get_lora_params(key):
    parts = key.split(".")
    layer_idx = None
    module_type = None
    lora_type = None

    for i, part in enumerate(parts):
        if part.isdigit():
            layer_idx = int(part)
        if part in ["lora_a", "lora_b"]:
            lora_type = part
            if i > 0:
                module_type = parts[i - 1]
            break

    return layer_idx, module_type, lora_type


lora_pairs = {}
for key in adapter_weights:
    layer_idx, module_type, lora_type = get_lora_params(key)
    if layer_idx is None or module_type is None or lora_type is None:
        continue

    pair_key = f"{layer_idx}.{module_type}"
    if pair_key not in lora_pairs:
        lora_pairs[pair_key] = {"layer_idx": layer_idx, "module_type": module_type}

    lora_pairs[pair_key][lora_type] = adapter_weights[key]

for pair_key, params in lora_pairs.items():
    layer_idx = params["layer_idx"]
    module_type = params["module_type"]

    if "lora_a" not in params or "lora_b" not in params:
        continue

    lora_a = params["lora_a"] * lora_scale
    lora_b = params["lora_b"]

    layer = base.model.layers[layer_idx]

    if "self_attn" in module_type:
        attn = layer.self_attn
        if "q_proj" in module_type:
            target = attn.q_proj
        elif "k_proj" in module_type:
            target = attn.k_proj
        elif "v_proj" in module_type:
            target = attn.v_proj
        elif "o_proj" in module_type:
            target = attn.o_proj
        else:
            continue
    elif "mlp" in module_type:
        mlp = layer.mlp
        if "gate_proj" in module_type:
            target = mlp.gate_proj
        elif "up_proj" in module_type:
            target = mlp.up_proj
        elif "down_proj" in module_type:
            target = mlp.down_proj
        else:
            continue
    else:
        continue

    if (
        target.weight.shape[0] == lora_a.shape[1]
        and target.weight.shape[1] == lora_b.shape[1]
    ):
        delta = torch.matmul(lora_b, lora_a)
        target.weight.data += delta.T

print("  Applied adapters")

print("Step 4: Saving fused model...")
base.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print(f"  Saved to: {output_dir}")

print()
print("Step 5: Converting to GGUF...")

cmd = [
    "/Users/igorlantushenko/train-llm/venv_torch/bin/python",
    "/Users/igorlantushenko/train-llm/llama.cpp/convert_hf_to_gguf.py",
    output_dir,
    "--outfile",
    output_gguf,
]

try:
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"  Saved: {output_gguf}")
except subprocess.CalledProcessError as e:
    print(f"  Failed: {e}")
    exit(1)

size_gb = os.path.getsize(output_gguf) / (1024**3)
print()
print("=" * 70)
print(f"COMPLETE! File: {output_gguf} ({size_gb:.2f} GB)")
print("=" * 70)
