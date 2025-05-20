#!/bin/bash

input_lengths=(128 1024)
output_lengths=(128 1024)
batch_sizes=(1 2 4 8 16 32 64 128)

for input_length in "${input_lengths[@]}"; do
  for output_length in "${output_lengths[@]}"; do
    for batch_size in "${batch_sizes[@]}"; do
      sleep 3
      num_prompts=$(( batch_size * 3))
      log_name="benchmarkdata_Llama-2-7b-chat-hf_inputlength_${input_length}_outputlength_${output_length}_batchsize_${batch_size}_numprompts_${num_prompts}.log"
      rm -f ${log_name}
      echo "Running benchmark with input_length=${input_length}, output_length=${output_length}, batch_size=${batch_size}, num_prompts=${num_prompts}" | tee -a ${log_name}
      # Run the benchmark client with the specified parameters
      ./run_benchmark_client.sh ${batch_size} $(( batch_size * 3)) ${input_length} ${output_length} >> ${log_name} 2>&1
    done
  done
done

