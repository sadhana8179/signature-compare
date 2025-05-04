from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim

def preprocess_image(path):
    img = Image.open(path).convert('L').resize((300, 100))
    return np.array(img)

def pixel_similarity(img1, img2):
    match = np.sum(img1 == img2)
    total = img1.size
    return (match / total) * 100

def ssim_score(img1, img2):
    return ssim(img1, img2)

def compare_signatures(ref_path, test_path, pixel_thresh=90, ssim_thresh=0.85):
    img1 = preprocess_image(ref_path)
    img2 = preprocess_image(test_path)

    pixel_sim = pixel_similarity(img1, img2)
    ssim_sim = ssim_score(img1, img2)

    if pixel_sim >= pixel_thresh and ssim_sim >= ssim_thresh:
        return "Genuine Signature"
    else:
        return "Forged Signature"
