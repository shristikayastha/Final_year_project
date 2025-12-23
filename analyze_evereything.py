import json
import os


print("WHISPER MODEL CHECKPOINT ANALYSIS")


# 1. Check what files exist
print("\n FILES IN CHECKPOINT:")
files = os.listdir(".")
for f in sorted(files):
    size = os.path.getsize(f)
    if size > 1024*1024:
        print(f"  {f} ({size/1024/1024:.1f} MB)")
    else:
        print(f"   {f} ({size/1024:.1f} KB)")

# 2. Model Configuration

print("MODEL CONFIGURATION:")

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    print(f"  Model Type: {config.get('model_type', 'Unknown')}")
    print(f"  Model Size: {config.get('_name_or_path', 'Unknown')}")
    print(f"  Vocab Size: {config.get('vocab_size', 'Unknown')}")
    print(f"  Max Length: {config.get('max_length', 'Unknown')}")
    print(f"  Architecture: {config.get('architectures', ['Unknown'])[0]}")
except:
    print("  Could not read config.json")

# 3. Training State

print(" TRAINING INFORMATION:")

try:
    with open('trainer_state.json', 'r') as f:
        trainer = json.load(f)
    print(f"  Total Training Steps: {trainer.get('global_step', 'Unknown')}")
    print(f"  Epochs Completed: {trainer.get('epoch', 'Unknown')}")
    print(f"  Best Metric: {trainer.get('best_metric', 'Unknown')}")
    print(f"  Best Model Checkpoint: {trainer.get('best_model_checkpoint', 'Unknown')}")
    
    if 'log_history' in trainer and len(trainer['log_history']) > 0:
        print(f"\n   Training Progress (last few entries):")
        for entry in trainer['log_history'][-5:]:
            step = entry.get('step', 'N/A')
            loss = entry.get('loss', entry.get('eval_loss', 'N/A'))
            print(f"    Step {step}: Loss = {loss}")
except:
    print("   Could not read trainer_state.json")

# 4. Tokenizer Info

print("TOKENIZER CONFIGURATION:")

try:
    with open('tokenizer_config.json', 'r') as f:
        tokenizer = json.load(f)
    print(f"  Tokenizer Type: {tokenizer.get('tokenizer_class', 'Unknown')}")
    print(f"  Model Max Length: {tokenizer.get('model_max_length', 'Unknown')}")
    
    # Check for language settings
    if 'language' in tokenizer:
        print(f"  Language: {tokenizer['language']}")
    if 'task' in tokenizer:
        print(f"  Task: {tokenizer['task']}")
except:
    print("   Could not read tokenizer_config.json")

# 5. Generation Config

print(" GENERATION SETTINGS:")

try:
    with open('generation_config.json', 'r') as f:
        gen_config = json.load(f)
    print(f"  Max Length: {gen_config.get('max_length', 'Unknown')}")
    if 'forced_decoder_ids' in gen_config:
        print(f"  Language/Task: Specified in forced_decoder_ids")
    if 'language' in gen_config:
        print(f"  Target Language: {gen_config['language']}")
    if 'task' in gen_config:
        print(f"  Task Type: {gen_config['task']}")
except:
    print("  Could not read generation_config.json")

# 6. Preprocessor Config

print(" AUDIO PREPROCESSING:")

try:
    with open('preprocessor_config.json', 'r') as f:
        prep_config = json.load(f)
    print(f"  Feature Extractor: {prep_config.get('feature_extractor_type', 'Unknown')}")
    print(f"  Sampling Rate: {prep_config.get('sampling_rate', 'Unknown')} Hz")
    print(f"  Chunk Length: {prep_config.get('chunk_length', 'Unknown')}")
except:
    print("   Could not read preprocessor_config.json")


print(" ANALYSIS COMPLETE!")
