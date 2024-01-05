import numpy as np
import cv2


class ImageEncryptor:
    def __init__(self, channel=2):
        """
        初始化加密类，默认替换图片的红色通道（R通道，索引为2）
        你可以通过修改channel参数来选择替换哪个通道（0: B, 1: G, 2: R）
        """
        self.channel = channel

    def string_to_matrix(self, s, shape):
        """
        将字符串转换为二维矩阵
        """
        # 创建一个全零矩阵，稍后将用字符串的字符填充
        matrix = np.zeros(shape, dtype=np.uint8)

        # 将字符串转换为字节数组
        byte_array = np.frombuffer(s.encode(), dtype=np.uint8)

        # 将字节数组填充到矩阵中，可能不完全填充
        matrix.flat[:len(byte_array)] = byte_array

        return matrix

    def encrypt_image(self, image_path, s):
        """
        加密图片
        """
        # 读取图片
        img = cv2.imread(image_path)
        h, w, _ = img.shape

        # 将字符串转换为二维矩阵
        text_matrix = self.string_to_matrix(s, (h * w,))  # 注意这里我们创建了一个一维矩阵
        text_matrix = text_matrix.reshape((h, w))  # 重新整形为二维矩阵

        # 替换图片的一个通道
        img[:, :, self.channel] = text_matrix

        return img

    def decrypt_image(self, encrypted_img):
        """
        解密图片
        """
        h, w, _ = encrypted_img.shape
        text_matrix = encrypted_img[:, :, self.channel].flatten()  # 展开为一维数组

        # 将一维数组转换回字符串
        s = text_matrix.tobytes().decode()

        # 去除字符串末尾可能的空字符
        s = s.rstrip('\x00')

        return s


if __name__ == '__main__':
    encryptor = ImageEncryptor(channel=2)  # 使用R通道
    message = input('your message:')
    encrypted_img = encryptor.encrypt_image('test_pic/input.jpg', str(message))
    cv2.imwrite('test_pic/encrypted.jpg', encrypted_img)

    decrypted_text = encryptor.decrypt_image(encrypted_img)
    print(decrypted_text)

    cv2.imshow('test', encrypted_img)
    cv2.waitKey(0)



