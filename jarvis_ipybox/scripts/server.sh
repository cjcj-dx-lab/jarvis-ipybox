#!/bin/bash

# 커스텀 커널 매니저 경로 추가
export PYTHONPATH=${HOME}:$PYTHONPATH

jupyter kernelgateway \
  --KernelGatewayApp.ip=0.0.0.0 \
  --KernelGatewayApp.port=8888 \
  --JupyterWebsocketPersonality.list_kernels=True \
  --KernelGatewayApp.kernel_manager_class=custom_kernel_manager.CustomMappingKernelManager
