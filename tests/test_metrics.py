import os
import warnings
import numpy as np
from PIL import Image
from metrics import images

def test_identical_images():
    np.random.seed(42)
    dummy  = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    image1 = Image.fromarray(dummy)
    image2 = image1.copy()
    
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    assert images.compute_ssim(image1, image2) == 1.0
    assert images.compute_psnr(image1, image2) == np.inf