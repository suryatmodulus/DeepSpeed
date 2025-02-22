'''
Copyright 2022 The Microsoft DeepSpeed Team
'''

from typing import Optional
import torch
from deepspeed.accelerator import get_accelerator
from deepspeed.ops.op_builder.builder_names import SpatialInferenceBuilder

spatial_cuda_module = None


def nhwc_bias_add(activation: torch.Tensor,
                  bias: torch.Tensor,
                  other: Optional[torch.Tensor] = None,
                  other_bias: Optional[torch.Tensor] = None) -> torch.Tensor:
    global spatial_cuda_module
    if spatial_cuda_module is None:
        spatial_cuda_module = get_accelerator().create_op_builder(
            SpatialInferenceBuilder).load()

    if other is None:
        return spatial_cuda_module.nhwc_bias_add(activation, bias)
    elif other_bias is None:
        return spatial_cuda_module.nhwc_bias_add_add(activation, bias, other)
    else:
        return spatial_cuda_module.nhwc_bias_add_bias_add(activation,
                                                          bias,
                                                          other,
                                                          other_bias)
