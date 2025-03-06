#!/bin/bash

jupyter kernelgateway \
  --KernelGatewayApp.ip=0.0.0.0 \
  --KernelGatewayApp.port=8888 \
  --JupyterWebsocketPersonality.list_kernels=True
