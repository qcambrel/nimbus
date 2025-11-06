import numpy as np
import matplotlib.cm as cm
from processing.scaling import scale
from utils.schemas import BlendContext

def blend(image: np.ndarray, context: BlendContext) -> np.ndarray:
    """
    Blends a color or alpha channel of an image based on intensity.
    Assumes alpha blending by default.

    Args:
        image (np.ndarray): The image to blend.
        context (BlendContext): The context for the blend.

    Returns:
        np.ndarray: The blended image.
    """
    if context.scale is None:
        context.scale = scale
        context.channel = 3

    if context.channel is None:
        context.channel = 3

    mappable = cm.ScalarMappable(norm=context.norm, cmap=context.cmap)
    rgba = mappable.to_rgba(image)
    rgba[:, :, context.channel] = context.scale(image, context.low, context.high)
    return rgba