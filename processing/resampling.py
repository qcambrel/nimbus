import numpy as np
from sunpy.image import resample as rs
from utils.schemas import ResampleContext

def resample(data: np.ndarray, shape: tuple, center=True):
    """
    Resamples an image to the given shape.

    Args:
        data (np.ndarray): The image to resample
        shape (tuple): The shape to resample to
        center (bool, optional): Whether to center the resampled image. Defaults to True.

    Returns:
        np.ndarray: The resampled image
    """
    return rs.resample(data, shape, center=center)

def batch_resample(batch: dict[str, np.ndarray], context: ResampleContext) -> dict[str, np.ndarray]:
    """
    Batches a resampling operation.

    Args:
        batch (dict[str, np.ndarray]): The batch of data to resample
        context (ResampleContext): The resampling context

    Returns:
        dict[str, np.ndarray]: The resampled batch
    """
    if context.resample is None:
        from processing.resampling import resample
        context.resample = resample

    batch["data"] = context.resample(batch["data"], context.shape, center=context.center)
    return batch