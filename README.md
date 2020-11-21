# AutomatedTesting2020

选题方向：移动自动化测试

## 参考文献

Yolov4：https://arxiv.org/abs/2004.10934

UIED：https://dl.acm.org/doi/10.1145/3368089.3417940

”Object Detection for Graphical User Interface: Old Fashioned or Deep Learning or a Combination?“https://dl.acm.org/doi/10.1145/3368089.3409691

## 第三方库版本
python=3.7.4

opencv-python=4.1.1.26

numpy=1.19.1

tensorflow-gpu=2.1.0

## 项目结构

Data：处理后的不同图片的控件和b_box信息、部分标注可视化的示例图片

Demo：Demo.wmv

Report：Report.md

Project:

​	prepare(数据标注部分)：

​		preprocess.py 预处理

​		annotation.py 可视化标注

​		classify.py 对控件类型分类并统计

​		check.py 将部分不是1080x1920的图片重新resize

​		format.py 将图片格式化为000001.jpg,000002.jpg的格式(用于构建		VOC2007数据集)

​		copy_image.py 复制图片到VOC2007/JPEGImage下

​		generate_xml 生成VOC2007/Annotations的xml文件

​		generate_txt 生成VOC2007/ImageSet下的相关txt文件

​	model(控件识别部分)

​		results：控件识别结果(使用uied工具)

​		configuration.zip 包含了模型训练权重和关键的配置文件

