#!/bin/bash
# get filter shared_gpt dataset
if [ ! -f ./filtered_sharedgpt_short_3000.json ]; then
  python get_filter_shared_gpt.py --tokenizer_name $MODEL_NAME
fi

concurrency=$1
num_prompts=$2
input_length=$3
output_length=$4
python benchmark_client.py \
  --dataset_path ./filtered_sharedgpt_short_3000.json \
  --backend paddle \
  --model_name /models/meta-llama/Llama-2-7b-chat \
  --num_prompts ${num_prompts} \
  --warmup_round 1 \
  --concurrency ${concurrency} \
  --host localhost \
  --port 9965 \
  --dataset_name random \
  --input_len ${input_length} \
  --min_dec_len ${output_length} \
  --max_dec_len ${output_length}

tail -n 2 /opt/output/log/workerlog.0 
