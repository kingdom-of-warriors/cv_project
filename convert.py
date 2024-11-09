import os
import xml.etree.ElementTree as ET

# 定义类别名称到数字的映射
names = ['root', 'level_0', 'level_1', 'level_2', 'clickable', 'level_0_scrollable', 'level_1_scrollable', 'disabled', 'selectable', 'scrollable']
class_mapping = {name: i for i, name in enumerate(names)}

def convert_xml_to_yolo(xml_file, img_size):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取图片尺寸
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)

    # 创建一个空列表来存储标签信息
    labels = []

    # 遍历所有的对象
    for obj in root.iter('object'):
        # 获取类别名称并转换为小写
        class_name = obj.find('name').text.lower()

        # 检查类别名称是否在映射表中
        if class_name in class_mapping:
            class_id = class_mapping[class_name]
        else:
            print(f"警告：类别 '{class_name}' 未在映射表中找到。")
            continue

        # 获取边界框坐标
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)

        # 计算中心点和宽高（相对于图片尺寸的比例）
        x_center = (xmin + xmax) / 2 / width
        y_center = (ymin + ymax) / 2 / height
        bbox_width = (xmax - xmin) / width
        bbox_height = (ymax - ymin) / height

        # 创建YOLO格式的标签字符串
        label_str = f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n"

        # 添加到标签列表
        labels.append(label_str)

    # 将标签列表转换为字符串
    labels_str = ''.join(labels)

    # 保存到.txt文件
    txt_file = os.path.splitext(xml_file)[0] + '.txt'
    with open(txt_file, 'w') as f:
        f.write(labels_str)

    return txt_file

# 主函数，用于处理文件夹中的所有XML文件
def main():
    # 指定包含XML文件的文件夹路径
    xml_folder = 'datasets/UI/train/labels_xml'
    # 指定输出文件夹路径
    output_folder = 'datasets/UI/train/labels'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 遍历文件夹中的所有XML文件
    for filename in os.listdir(xml_folder):
        if filename.endswith('.xml'):
            xml_file = os.path.join(xml_folder, filename)
            # 读取XML文件并获取图片尺寸
            tree = ET.parse(xml_file)
            root = tree.getroot()
            size = root.find('size')
            img_width = int(size.find('width').text)
            img_height = int(size.find('height').text)

            # 转换XML文件为YOLO格式的TXT文件
            txt_file = convert_xml_to_yolo(xml_file, (img_width, img_height))

            # 将TXT文件保存到输出文件夹
            output_path = os.path.join(output_folder, os.path.basename(txt_file))
            with open(txt_file, 'r') as src:
                with open(output_path, 'w') as dst:
                    dst.write(src.read())

if __name__ == '__main__':
    main()