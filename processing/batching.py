# DEPRECIATED

import ray
import numpy as np
from utils.schemas import BatchContext

def batch_process(images: list[np.ndarray], func: callable, context: BatchContext) -> ray.data.Dataset:
    """
    Batches a list of images and applies a function to each batch.
    Batching with Ray Data improves performance.
    """
    ds = ray.data.from_numpy(images).map_batches(
        func,
        fn_args=context.fn_args,
        fn_kwargs=context.fn_kwargs,
        batch_size=context.batch_size,
        num_cpus=context.num_cpus,
        num_gpus=context.num_gpus,
        concurrency=context.concurrency,
        batch_format=context.batch_format
    )
    return ds