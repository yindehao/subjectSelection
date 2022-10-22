alter table subject
modify column innovation
varchar(100) default null comment '创新点';


insert into subject(subject_id, subject_name, description, language,
                    platform, min_person, max_person, innovation,
                    max_group, origin,
                    created_time, last_modified_time, version)
values (5,'用于量子精密测量仪表的人机交互软件系统设计',
        '基于科大自研的量子精密测量仪器，完成系统人机界面前后端设计与开发，包括实验设
定、数据采集、数据存储和显示等功能，并支持与设备的实时交互，实现系统的实时控制。',
        'Python, SQL','Pycharm, Mysql',4,4,null,1,'导师课题',now(),now(),1),
    (6,'用于仪表检测领域的自动读数与识别系统设计','研究图像识别+NLP 结合的 OCR 技术，在 PC 平台完成仪表检测场景中的区域检测、特
征提取、字符识别、检测报表生成等功能开发。技术路线涉及深度学习模型的定义、训练和
部署，更进一步地可完成在嵌入式平台中的移植。
课题基础：在过去几年，已有两个版本的系统原型，在此基础上进一步实验',
     'Python, C/C++, SQL','Linux, OpenCV',4,4,
'创新点：结合特定业务领域文本约束的的图像识别，支持自动识别和报表生成功能',1,'导师课题',now(),now(),1),
    (7,'基于机器学习的智能整形控制系统设计','研究典型机器学习模型，完成某智能整形装备的输入数据处理，并结合控制量、加工结
果等标签数据，完成模型定义、训练和部署，实现对控制量的自动预测和调整，完成模型训
练软件的前后端开发。
技术路线 A：基于多特征数据回归分析，对已有 MLP 模型进行改进和再实验
课题基础：在过去几年，已有一个 MLP 模型的原型系统，具有成熟实验环境','Python, C/C++, SQL','Pycharm, Mysql',4,4,null,1,
'导师课题',now(),now(),1),
    (8,'基于机器学习的智能整形控制系统设计','研究典型机器学习模型，完成某智能整形装备的输入数据处理，并结合控制量、加工结
果等标签数据，完成模型定义、训练和部署，实现对控制量的自动预测和调整，完成模型训
练软件的前后端开发。
技术路线 B：基于数据序列特征分析，对已有 LSTM 模型进行改进和再实验
课题基础：在过去几年，已有一个 LSTM 模型的原型系统，具有成熟实验环境','Python, C/C++, SQL','Pycharm, Mysql',4,4,null,1,
'导师课题',now(),now(),1),
    (9,'基于机器学习的智能整形控制系统设计','研究典型机器学习模型，完成某智能整形装备的输入数据处理，并结合控制量、加工结
果等标签数据，完成模型定义、训练和部署，实现对控制量的自动预测和调整，完成模型训
练软件的前后端开发。
技术路线 C：基于系统的自学习方法，实现强化学习建模和控制系统开发
课题基础：已有面向机器人的强化学习原型系统，需针对该场景进行模型适配和算法调试','Python, C/C++, SQL','Pycharm, Mysql',4,4,null,1,
'导师课题',now(),now(),1),
    (10,'基于华为云平台的产品缺陷自动检测系统设计','面向实际产线中采样的海量图像，进行图像自动化标注、图像增强、特征检测和语义判
别，在华为云上完成图像处理算法或机器学习模型的定义、训练和部署，完成系统的前后端
设计与开发，前端界面中支持缺陷类型的设定及处理前后图像的显示。',
     'Python, C/C++, SQL','Linux, OpenCV',4,4,
'在华为 SDK 上进行经典数字图像处理方法与多种机器学习模型的综合实践',1,'导师课题',now(),now(),1),
    (11,'基于人体姿态估计的 AI 健身系统的设计与实现','计算机视觉技术的发展改变了人们的生活，将视觉理解技术应用于生活才能
真正体现其价值。我们基于人体姿态估计的视觉技术，开发了能够辅助仰卧起坐、
俯卧撑、深蹲等运动计数的应用产品。该产品适合在进行相关健身动作时使用，
能够实时、高效地计算人体运动的个数。
参考资料：https://www.cnblogs.com/ykzhou/p/16693088.html','Python, C/C++, SQL','Linux, OpenCV',4,4,null,1,
     '导师课题',now(),now(),1),
    (12,'基于机器学习算法的（影视、旅游、…）大数据分析','本课题采用机器学习算法对爬取的用户评论数据进行分析。',
     'Python, C/C++, SQL','Linux, OpenCV',4,4,null,1,
     '导师课题',now(),now(),1),
    (13,'基于情感词典的（影视、旅游、…）大数据分析','本课题采用情感词典的方法对爬取的用户评论数据进行分析。',
     'Python, C/C++, SQL','Linux, OpenCV',4,4,null,1,
     '导师课题',now(),now(),1),
    (14,'移动终端上的智能证件照系统的设计与实现',
     '在移动终端上，对普通照片进行智能识别，对头像区域抠图，制作出相应的证件照，支持一寸二寸等尺寸，支持证件照换底色。',
     'Java, Kotlin, SQL','Android Studio, OpenCV',4,4,null,1,
     '导师课题',now(),now(),1),
    (15,'（影视、旅游、某类商品…）推荐系统的设计与实现','本课题通过数据抓取、分析、处理等过程实现一个完整的面向主题的推荐系统。',
     'Python, C/C++, SQL','Linux, OpenCV',4,4,null,1,
     '导师课题',now(),now(),1);

insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000002',5,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000002',6,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000002',7,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000002',8,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000002',9,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000002',10,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000003',11,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000003',12,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000003',13,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000003',14,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000003',15,false,1);