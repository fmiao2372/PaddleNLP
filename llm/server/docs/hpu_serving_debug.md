## HPU Serving

### Image
docker run -it --runtime=habana -v /mnt/disk2/models:/models --name  hpu-paddle-serving-debug -d -e HABANA_VISIBLE_DEVICES=all -e OMPI_MCA_btl_vader_single_copy_mechanism=none --cap-add=sys_nice --net=host --ipc=host hpu-paddle-serving-debug:latest /bin/bash

### Model path
Host: /mnt/disk2/models

Conatiner: /models

### Code workspace
``` bash
/opt/source/PaddleNLP
/opt/source/PaddleCustomDevice
```
To update to the latest code, you can use the paddle_pull.sh script.

### Update settings
set hpu device in /usr/local/bin/start_server

``` bash
export FLAGS_selected_intel_hpus=0
```

### Start server
``` bash
cd /opt/output
start_server
```
You can edit the start_server script and update the related settings accordingly.

The following log shows that the triton server has started successfully.
``` bash
......
[2025-04-15 06:11:10,380] [    INFO] triton_server.py:259 - Launch HTTP server for push mode success, http_url:http://127.0.0.1:9965/v1/chat/completions
[2025-04-15 06:11:10,381] [    INFO] triton_server.py:264 - init push server success
[2025-04-15 06:11:10,381] [    INFO] triton_server.py:196 - Init triton server success
```
### Client 
Use the following command to send a request.
``` bash
curl 127.0.0.1:9965/v1/chat/completions   -H'Content-Type: application/json'   -d'{"text": "hello, llm"}'
```
### Log check
For PaddleNLP debugging, you can refer to the launch_infer.log and infer.log located in the /opt/log directory.

### Stop server
``` bash
ps aux | egrep -i "paddle|spawn_main|triton" | grep -v grep | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
```