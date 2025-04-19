from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import numpy as np

digits = load_digits()
print(f"画像の数: {len(digits.images)}")
print(f"ラベル例: {digits.target[:10]}")

# サンプル表示
plt.imshow(digits.images[0], cmap='gray')
plt.title(f"Label: {digits.target[0]}")
plt.show()

import cv2

# ランダムに5個選んで横に並べた画像を作る
indices = np.random.choice(len(digits.images), 5, replace=False)
composite = np.hstack([digits.images[i] for i in indices])
labels = [digits.target[i] for i in indices]

# OpenCVで扱えるようuint8化
composite = np.uint8(255 * composite / np.max(composite))

cv2.imshow("Composed Digits", composite)
cv2.waitKey(0)
cv2.destroyAllWindows()

w = digits.images[0].shape[1]  # 各画像の幅（例：8）
for i in range(5):
    x = i * w
    y = 0
    roi = composite[y:y+w, x:x+w]
    
    # 矩形を描画
    cv2.rectangle(composite, (x, y), (x + w, y + w), (255,), 1)
    cv2.putText(composite, str(labels[i]), (x+2, y+12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,), 1)

cv2.imshow("Detected Digits", composite)
cv2.waitKey(0)
cv2.destroyAllWindows()
