import numpy as np
import cv2


class ImageEncryptor:
    def __init__(self, channel=2):
        """
        初始化加密类，默认替换图片的蓝色通道（B通道，索引为0）
        你可以通过修改channel参数来选择替换哪个通道（0: B, 1: G, 2: R）
        """
        self.channel = channel

    def string_to_matrix(self, s, shape):
        """
        将字符串转换为二维矩阵
        """
        matrix = np.full(shape, ord(' '))  # 使用空格的ASCII值填充矩阵
        idx = 0
        for i in range(shape[0]):
            for j in range(shape[1]):
                if idx < len(s):
                    matrix[i, j] = ord(s[idx])
                    idx += 1
                else:
                    break
        return matrix

    def encrypt_image(self, image_path, s):
        """
        加密图片
        """
        # 读取图片
        img = cv2.imread(image_path)
        h, w, _ = img.shape

        # 将字符串转换为二维矩阵
        text_matrix = self.string_to_matrix(s, (h, w))

        # 替换图片的一个通道
        img[:, :, self.channel] = text_matrix % 256  # 确保值在0-255范围内

        return img

    def decrypt_image(self, encrypted_img):
        """
        解密图片
        """
        h, w, _ = encrypted_img.shape
        text_matrix = encrypted_img[:, :, self.channel]

        s = ''
        for i in range(h):
            for j in range(w):
                if text_matrix[i, j] != ord(' '):  # 如果不是空格的ASCII值
                    s += chr(text_matrix[i, j])
                else:
                    break  # 假设空格之后没有更多的字符
        return s.rstrip()  # 移除字符串右侧的空格（如果有的话）


# test
if __name__ == '__main__':
    encryptor = ImageEncryptor(channel=0)  # 使用B通道
    encrypted_img = encryptor.encrypt_image('test_pic/input.jpg', 'Hello, World!')
    cv2.imwrite('encrypted.jpg', encrypted_img)

    decrypted_text = encryptor.decrypt_image(encrypted_img)
    print(decrypted_text)
