import os
import re
import csv

log_dir = '.' 
output_csv = 'parsed_logs.csv'

log_file_pattern = re.compile(r'benchmarkdata_Llama-2-7b-chat-hf_inputlength_(\d+)_outputlength_(\d+)_batchsize_(\d+)_numprompts_(\d+)\.log')

qps_pattern = re.compile(r'QPS:\s+(\d+\.\d+)')
real_output_tokens_pattern = re.compile(r'Real Output Tokens/s:\s+(\d+\.\d+)')
first_token_latency_pattern = re.compile(r'First Token Latency \(min, max, avg\):\s+(\d+\.\d+),\s+(\d+\.\d+),\s+(\d+\.\d+)')
total_token_latency_pattern = re.compile(r'Total Token Latency \(min, max, avg\):\s+(\d+\.\d+),\s+(\d+\.\d+),\s+(\d+\.\d+)')
infer_time_pattern = re.compile(r'\[.*\] \[.*\] infer\.py:\d+ - _infer average time:\s+(\d+\.\d+) ms')
step_cuda_time_pattern = re.compile(r'\[.*\] \[.*\] infer\.py:\d+ - step_cuda average time:\s+(\d+\.\d+) ms')

with open(output_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Log File', 'Input Length', 'Output Length', 'Batch Size', 'Num Prompts', 'QPS', 'Real Output Tokens/s', 'First Token Latency Min', 'First Token Latency Max', 'First Token Latency Avg', 'Total Token Latency Min', 'Total Token Latency Max', 'Total Token Latency Avg', 'Infer Time', 'StepPaddle Time'])

    for log_file in os.listdir(log_dir):
        match = log_file_pattern.match(log_file)
        if match:
            input_length, output_length, batch_size, num_prompts = match.groups()
            log_path = os.path.join(log_dir, log_file)
            with open(log_path, 'r') as f:
                lines = f.readlines()[-10:] 

                qps = real_output_tokens = first_token_latency_min = first_token_latency_max = first_token_latency_avg = ''
                total_token_latency_min = total_token_latency_max = total_token_latency_avg = infer_time = step_cuda_time = ''

                for line in lines:
                    if qps_match := qps_pattern.search(line):
                        qps = qps_match.group(1)
                    elif real_output_tokens_match := real_output_tokens_pattern.search(line):
                        real_output_tokens = real_output_tokens_match.group(1)
                    elif first_token_latency_match := first_token_latency_pattern.search(line):
                        first_token_latency_min = first_token_latency_match.group(1)
                        first_token_latency_max = first_token_latency_match.group(2)
                        first_token_latency_avg = first_token_latency_match.group(3)
                    elif total_token_latency_match := total_token_latency_pattern.search(line):
                        total_token_latency_min = total_token_latency_match.group(1)
                        total_token_latency_max = total_token_latency_match.group(2)
                        total_token_latency_avg = total_token_latency_match.group(3)
                    elif infer_time_match := infer_time_pattern.search(line):
                        infer_time = infer_time_match.group(1)
                    elif step_cuda_time_match := step_cuda_time_pattern.search(line):
                        step_cuda_time = step_cuda_time_match.group(1)

                csvwriter.writerow([log_file, input_length, output_length, batch_size, num_prompts, qps, real_output_tokens, first_token_latency_min, first_token_latency_max, first_token_latency_avg, total_token_latency_min, total_token_latency_max, total_token_latency_avg, infer_time, step_cuda_time])

print(f'Parsed log data has been written to {output_csv}')
