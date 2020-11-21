# AutomatedTesting2020

姓名：梅凯

学号：181840164

选题方向：移动自动化测试

## 模型分析

### 模型结构

Project下分为prepare(数据标注预处理)和model(模型相关的配置和权重文件)

#### model

由于cuda9.0版本与我的笔记本gpu不兼容，所以无法使用兼容的cuda版本较低的yolov3，而是采用与我的gpu driver能够兼容的yolov4

yolov4的具体结构如图

![](https://github.com/dongyuanjushi/ATMobileTesting2020/blob/master/Report/yolov4%E6%A8%A1%E5%9E%8B%E7%BB%93%E6%9E%84.jpg)

### 运行步骤

#### 数据预处理

工作区为Project/prepare

1. 将原始图片的jpg和json放置在Data/data下，运行format.py对数据名称格式化用于后续构建VOC2007数据集
2. 运行preprocess对控件进行分类以及对b_box进行去重以及合并，生成数据文件Data/all_data.json和Data/all_data.txt
3. (非必须)运行classify.py可以查看控件数据的分类情况(我分了15类，包括ImageView,TextView,Button等常用控件)，详情见Data/classified.txt
4. 按顺序依次运行copy_image,generate_xml和generate_txt.py在Data下构建VOC2007的数据集

ps：所用的数据集进行了一定的人工筛选，将b_box标注较差的数据去除之后共848个图片样本

#### 模型训练

保存的文件在Project/model下

由于模型训练使用的为c++版本的darknet/yolov4(我尝试过tensorflow和pytorch版本的，训练速度都很慢)，所以在model目录下没有放置完整的模型，而只放置了训练后的权重文件和关键的配置文件，详细的配置信息参考https://github.com/AlexeyAB/darknet/blob/master/README.md

### 实验验证

#### 数据标注

根据我调整后的b_box进行可视化(采用cv2)，可视化代码在Project/prepare/annotation.py文件中

#### 控件识别



### 相关参考文献

Yolov4：https://arxiv.org/abs/2004.10934



### 评估指标及含义

### 验证结果

### 结果示例

### 个人感想



