# 添加院系：软件学院，计算机学院，先研院
insert into dept(dept_id, dept_name, city)
values(1,'软件学院 苏州','苏州'),
      (2,'软件学院 合肥','苏州'),
      (3,'计算机学院','合肥'),
      (4,'先进技术研究院','合肥');

# 添加学生信息
insert into student(student_id, team_id, dept_id, password,
                    phone_number, email, description,
                    gender, birthday, student_name, student_type,
                    student_class, resume)
VALUES('SA22225453', null, '1','SA22225453',
       19956704343,'yindehao@ustc.edu','',
       true,date('2000-01-01'),'殷德好','硕士研究生',
       '2022级大数据二班',null),
    ('SA22225192', null, '1','SA22225192',
       15170292971,'huangxinwei@ustc.edu','',
       true,date('2000-01-01'),'黄鑫伟','硕士研究生',
       '2022级大数据一班',null),
    ('SA22225149', null, '1','SA22225149',
       18342294949,'duanyifan@ustc.edu','',
       true,date('2000-01-01'),'段逸凡','硕士研究生',
       '2022级大数据一班',null),
    ('SA22225256', null, '1','SA22225192',
       19966152567,'huangxinwei@ustc.edu','',
       true,date('2000-01-01'),'刘玮祎','硕士研究生',
       '2022级网安一班',null);

# 添加导师信息
insert into instructor(instructor_id, dept_id, password,
                       phone_number, email, description,
                       gender, birthday, instructor_name, title)
values('TA00000001',1,'TA00000001','055168839314','jfzhai@ustc.edu.cn',null,
       false,'1983-01-01','翟建芳',null),
    ('TA00000002',1,'TA00000002','055168839303','gavin@ustc.edu.cn',null,
       false,'1985-01-01','赵振刚',null),
    ('TA00000003',1,'TA00000003','055168839304','ywyu@ustc.edu.cn',null,
       false,'1983-01-01','余艳玮',null);


# 插入课题
insert into subject(subject_id, subject_name, description, language,
                    platform, min_person, max_person, innovation,
                    max_group, origin,
                    created_time, last_modified_time, version)
values (1,'基于RISC-V和AI计算的数字系统开发平台设计',
        '本项目融合当前AI计算模式，结合RISC-V开源指令集及SOC验证平台，构建一个数字设计平台。
本平台，遵循EDA经典设计流程，完成既定功能的片上系统的开发，形成一套指令集下的CPU与AI计算单元相辅相成的架构。
地点：苏州
技术要求：数字系统设计基础知识、C语言基础、机器学习及优化算法',
        'C语言基础',null,3,4,null,4,'导师课题',now(),now(),1),
    (2,'在线实验平台的搭建','当前在线教育及微课、慕课、翻转课堂成为教学实践探索的热点。
本项目基于同学们自主开发的课程实验demo或实践项目，
使用常见的前后端开发工具或框架、数据库MySQL、Mongodb等，
实现作业提交、在线代码提交和调试结果展示、根据输出自动划定等次、题库积累和随机分配等功能。
地点：苏州',
     'C++、java、js、sql', null,3,4,null,3,'导师课题',now(),now(),1),
    (3,'基于Python的实验库设计及实现',
    '针对Python的知识点，形成全面的实验库覆盖，包括web开发、科学计算、人工智能、游戏开发等应用方向。
本题目需要同学们编写前后端实验平台，具备前后端开发知识、数据库访问技术和软件架构设计。并熟悉Python的常用知识点，进行针对性demo开发。
地点：苏州',
     'Python、sql、web技术等',null,3,4,null,4,'导师课题',now(),now(),1),
    (4,'基于FPGA的图像传输系统实现',
'描述：本题目基于ZYNQ7000系列的FPGA平台，控制实现图像格式的生成，包括bmp格式、jpg格式、png格式等。同时，该系统通过FPGA控制，实现图像的传输显示。
本题目需要同学们学会使用HDL和C语言，了解FPGA的运行和控制原理，进而锻炼硬件设计的能力。
地点：苏州；','C、HDL、FPGA等',null,3,4,null,4,'导师课题',now(),now(),1);

# 将课题存为草稿
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000001',1,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000001',2,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000001',3,false,1);
insert into release_subject(instructor_id, subject_id, released, version)
VALUES('TA00000001',4,false,1);