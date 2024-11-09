import os
import shutil

def convert_dataset(src_dir, train_dir, label_dir, start_index=1):
    # 确保输出目录存在
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    # 初始化文件索引
    file_index = start_index

    # 遍历源目录
    for root, dirs, files in os.walk(src_dir):
        for file in sorted(files):
            if file.endswith('.png'):
                # 构建.xml文件的名称
                xml_file = file.replace('.png', '.xml')
                # 检查.xml文件是否存在
                if xml_file in files:
                    # 构建新的文件名（frame_i.png和frame_i.xml）
                    new_filename = f"frame_{file_index:03d}.png"  # 格式化索引为三位数，不足前面补零
                    new_xml_filename = f"frame_{file_index:03d}.xml"
                    # 构建目标路径
                    train_file = os.path.join(train_dir, new_filename)
                    label_file = os.path.join(label_dir, new_xml_filename)
                    # 复制文件
                    shutil.copy(os.path.join(root, file), train_file)
                    shutil.copy(os.path.join(root, xml_file), label_file)
                    print(f"文件 {file} 和 {xml_file} 已转换并移动到 {train_file} 和 {label_file}")
                    # 递增文件索引
                    file_index += 1

# 设置源目录、训练目录和标签目录的路径
source_dataset_dir = 'v1'  # 源数据集路径
train_images_dir = 'datasets/UI/train/images'                  # 训练图片路径
label_annotations_dir = 'datasets/UI/train/labels_xml'  

convert_dataset(source_dataset_dir, train_images_dir, label_annotations_dir)