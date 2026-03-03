import json
import os

# Convert data.jsonl to training format for mlx_lm
# Need to convert to text format with proper prompt/completion structure

input_file = "/Users/igorlantushenko/train-llm/training_data/data.jsonl"
output_file = "/Users/igorlantushenko/train-llm/training_data/train.jsonl"

with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    for line in f_in:
        data = json.loads(line.strip())
        messages = data.get('messages', [])
        
        # Extract system, user, assistant
        system_content = ""
        user_content = ""
        assistant_content = ""
        
        for msg in messages:
            role = msg.get('role', '')
            content = msg.get('content', '')
            if role == 'system':
                system_content = content
            elif role == 'user':
                user_content = content
            elif role == 'assistant':
                assistant_content = content
        
        # Format for training - use chat template
        if system_content and user_content and assistant_content:
            text = f"<|im_start|>system\n{system_content}<|im_end|>\n<|im_start|>user\n{user_content}<|im_end|>\n<|im_start|>assistant\n{assistant_content}<|im_end|>"
            f_out.write(json.dumps({"text": text}) + "\n")

print(f"Converted {output_file}")
