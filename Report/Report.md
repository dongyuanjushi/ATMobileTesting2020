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

1. 训练模型：

   由于模型训练使用的为c++版本的darknet/yolov4(我尝试过tensorflow和pytorch版本的，训练速度都很慢)，所以在model目录下没有放置完整的模型，而只放置了训练后的权重文件和关键的配置文件，详细的配置信息参考https://github.com/AlexeyAB/darknet/blob/master/README.md

2. 使用Web的检测工具比较不同的检测方法

### 实验验证

#### 数据标注

根据我调整后的b_box进行可视化(采用cv2)判断标注情况，可视化代码在Project/prepare/annotation.py文件中

#### 控件识别

1. 通过YOLOv4深度学习框架进行训练
2. 使用可视化工具比较YOLO和新兴检测方法(传统OCR+深度学习分类)的检测结果

### 相关参考文献

Yolov4：https://arxiv.org/abs/2004.10934

UIED：https://dl.acm.org/doi/10.1145/3368089.3417940

”Object Detection for Graphical User Interface: Old Fashioned or Deep Learning or a Combination?“https://dl.acm.org/doi/10.1145/3368089.3409691

### 评估指标及含义

mAP：(Mean Average Precision) 所有类别的平均精度求和除以所有类别

ps：在我的模型训练中由于训练情况较差，所以未采用mAP进行大规模评估

### 验证结果

#### 数据标注

通过不同的分类标注尝试之后，发现控件分为12~15类之后的标注结果较好(我使用的为15类)

通过对b_box合并去重的尝试，发现宽的阈值设定为10，长的阈值设为15去重的效果较好，不过json中存在很多极端情况，详细的合并规则见Project/prepare/process.py

#### 控件识别

1. Yolov4训练：

   通过设立不同的learning_rate(0.001,0.0005,0.0001)发现学习率高的情况下会梯度爆炸(nan)

   总体的训练结果很不好，大多数图片都检测不出b_box

   猜测原因：

   1. 训练次数不够(2000 iteration)，(YOLOv4层数较多：161，gpu性能不够)
   2. 源数据里有很多小控件以及极其相似的控件
   3. 只采用深度学习模型的方式难以学习到GUI控件的检测(只有b_box，控件检测可能需要大量数据预训练以及其他的检测方法)

2. UIED在线GUI检测工具使用

   对比了yolo的检测情况和uied的检测情况

### 结果示例

#### 数据标注

![](https://github.com/dongyuanjushi/ATMobileTesting2020/blob/master/Data/example/000021.jpg)

![](https://github.com/dongyuanjushi/ATMobileTesting2020/blob/master/Data/example/000035.jpg)

#### UIED检测

使用UIED方法

![](https://github.com/dongyuanjushi/ATMobileTesting2020/blob/master/Project/model/results/UIED/detect.PNG)

使用YOLO方法

![](https://github.com/dongyuanjushi/ATMobileTesting2020/blob/master/Project/model/results/YOLO/detect.PNG)

### 个人感想

1. 深度学习模型对于GUI检测的效果相对一般，可能需要大量的预训练模型
2. json标注然后进行筛选的方法标注情况较差，为了提高精度还是需要以人工标注为主
3. 预先将文本与非文本控件分离(OCR)，然后划分不同区域和可能出现的控件信息进行预测，能够提高检测效果

ps：深度学习没钱的人是不配学的(x) ——来自一个训练两天只有2000iteration而且效果很烂的废物

