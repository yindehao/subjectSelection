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