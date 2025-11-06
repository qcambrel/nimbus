import numpy as np

def scale(image: np.ndarray, low: float = None, high: float = None) -> np.ndarray:
    """
    Scales an image to the range [0, 1].
    Scaling alpha channels enables intensity based alpha blending.

    Args:
        image (np.ndarray): The image to scale
        low (float, optional): The low value to scale to. Defaults to None.
        high (float, optional): The high value to scale to. Defaults to None.

    Returns:
        np.ndarray: The scaled image
    """
    if low is None:
        low = np.min(image)
    if high is None:
        high = np.max(image)
        
    scaled_image = (image - low) / (high - low) * 255
    scaled_image = np.clip(scaled_image, 0, 255) / 255
    return scaled_image