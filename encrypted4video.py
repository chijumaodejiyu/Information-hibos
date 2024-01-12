import time

import numpy as np
import cv2


class VideoEncryptor:
    def __init__(self, channel=2):
        """
        初始化加密类，默认替换视频的红色通道（R通道，索引为2）
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

    def encrypt_video(self, video_path, s):
        """
        加密视频
        """
        # 读取视频帧并获取帧大小和帧数
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 将字符串转换为二维矩阵
        text_matrix = self.string_to_matrix(s, (frame_height * frame_width,))  # 注意这里我们创建了一个一维矩阵
        text_matrix = text_matrix.reshape((frame_height, frame_width))  # 重新整形为二维矩阵

        # 打开输出视频文件并写入加密后的视频帧
        out = cv2.VideoWriter('test_pic/encrypted_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

        for i in range(frame_count):
            ret, frame = cap.read()
            if not ret:  # 如果无法读取帧，则跳过该帧
                continue
                # 替换视频的一帧的某个通道
            frame[:, :, self.channel] = text_matrix
            out.write(frame)  # 将加密后的帧写入输出视频文件
            print("加密视频已写入磁盘")

        cap.release()  # 释放视频捕获对象
        out.release()  # 释放视频写入对象

    def decrypt_video(self, encrypted_video_path):
        """
        解密视频
        """
        # 读取加密的视频帧并获取帧大小和帧数
        cap = cv2.VideoCapture(encrypted_video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 初始化变量来存储提取的信息
        extracted_text = ""

        for i in range(frame_count):
            ret, frame = cap.read()
            if not ret:  # 如果无法读取帧，则跳过该帧
                continue
                # 从加密的帧中提取信息
            if self.channel == 0:  # B通道
                extracted_text += frame[:, :, 0].flatten().tobytes().decode('utf-8') + " "
            elif self.channel == 1:  # G通道
                extracted_text += frame[:, :, 1].flatten().tobytes().decode('utf-8') + " "
            else:  # R通道
                extracted_text += frame[:, :, 2].flatten().tobytes().decode('utf-8') + " "

        cap.release()  # 释放视频捕获对象

        # 去除末尾的空格并返回提取的信息
        return extracted_text.rstrip()


if __name__ == "__main__":
    encryptor = VideoEncryptor(channel=2)  # 使用R通道
    test_video_path = 'test_pic/test.mp4'
    encrypt_video_path = 'test_pic/encrypted_video.mp4'
    message = input('your message:')
    encryptor.encrypt_video(test_video_path, message)
    time.sleep(3)
    print(encryptor.decrypt_video(encrypt_video_path))
    cv2.waitKey(0)



