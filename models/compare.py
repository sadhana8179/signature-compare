import cv2
from skimage.metrics import structural_similarity as ssim

def compare_signatures(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    img1 = cv2.resize(img1, (300, 100))
    img2 = cv2.resize(img2, (300, 100))

    score, _ = ssim(img1, img2, full=True)
    return round(score * 100, 2)
