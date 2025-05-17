import cv2
import sys
import os

def resize_image(input_path, output_path=None, width=398, height=575):
    """
    将输入图片压缩为指定尺寸
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径，默认为None（覆盖原图）
    :param width: 输出图片宽度
    :param height: 输出图片高度
    :return: True成功，False失败
    """
    try:
        # 读取图片
        img = cv2.imread(input_path)
        if img is None:
            print(f"错误：无法读取图片 {input_path}")
            return False
        
        # 调整图片大小 (保持纵横比可以使用 INTER_AREA 效果更好)
        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        
        # 如果没有指定输出路径，则覆盖原图
        if output_path is None:
            output_path = input_path
            
        # 保存图片
        cv2.imwrite(output_path, resized_img)
        print(f"已将图片压缩为 {width}×{height} 并保存至: {output_path}")
        return True
        
    except Exception as e:
        print(f"处理图片时出错: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python resize_image.py 输入图片路径 [输出图片路径]")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_path):
        print(f"错误: 找不到文件 {input_path}")
        sys.exit(1)
        
    success = resize_image(input_path, output_path)
    sys.exit(0 if success else 1)