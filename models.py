# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, LargeBinary, String, Table, Text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import RepresentableBase

Base = declarative_base(cls=RepresentableBase)
metadata = Base.metadata


class Dept(Base):
    __tablename__ = 'dept'
    __table_args__ = {'comment': '导师和学生所属院系\\r\\nvarchar长度按照 字长度计算'}

    dept_id = Column(BigInteger, primary_key=True)
    dept_name = Column(String(8), comment='软件学院')
    city = Column(String(4), comment='合肥、苏州')


class Message(Base):
    __tablename__ = 'message'
    __table_args__ = {'comment': '消息表'}

    message_id = Column(BigInteger, primary_key=True)
    from_user = Column(String(16))
    to_user = Column(String(16))
    title = Column(String(100))
    content = Column(Text)


class Subject(Base):
    __tablename__ = 'subject'
    __table_args__ = {'comment': '工程实践题目表。属性有：\\r\\nid，\\r\\n题目名称，\\r\\n题目介绍，\\r\\n题目来源（企业'}

    subject_id = Column(BigInteger, primary_key=True)
    subject_name = Column(String(30), nullable=False)
    description = Column(Text)
    language = Column(String(30))
    platform = Column(String(30))
    min_person = Column(Integer)
    max_person = Column(Integer)
    innovation = Column(String(100))
    max_group = Column(Integer)
    origin = Column(String(10), comment='企业课题、导师课题')
    created_time = Column(DateTime)
    last_modified_time = Column(DateTime)
    version = Column(BigInteger)


class Instructor(Base):
    __tablename__ = 'instructor'
    __table_args__ = {
        'comment': '指导教师，负责发布选题和确认小组选题情况。\\r\\n属性包括：\\r\\nid，\\r\\n导师姓名，\\r\\n                               -&#'}

    instructor_id = Column(String(16), primary_key=True)
    dept_id = Column(ForeignKey('dept.dept_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    password = Column(String(300), comment='哈希后的密文')
    phone_number = Column(String(16))
    email = Column(String(32))
    description = Column(Text)
    gender = Column(TINYINT(1))
    birthday = Column(Date)
    instructor_name = Column(String(16))
    title = Column(String(8))

    dept = relationship('Dept')


class Team(Base):
    __tablename__ = 'team'
    __table_args__ = {'comment': '小组'}

    team_id = Column(BigInteger, primary_key=True)
    subject_id = Column(ForeignKey('subject.subject_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    team_name = Column(String(20))
    leader_id = Column(String(16))
    version = Column(BigInteger, comment='每次加入/删除队员会更改版本号')

    subject = relationship('Subject')


class ReleaseSubject(Base):
    __tablename__ = 'release_subject'
    __table_args__ = {'comment': '一个导师可以发布多个题目。\\r\\n也可以有多个导师联合指导题目'}

    instructor_id = Column(ForeignKey('instructor.instructor_id', ondelete='RESTRICT', onupdate='RESTRICT'),
                           primary_key=True, nullable=False)
    subject_id = Column(ForeignKey('subject.subject_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
                        nullable=False, index=True)
    released = Column(TINYINT(1), comment='可以存为草稿')
    version = Column(BigInteger)

    instructor = relationship('Instructor')
    subject = relationship('Subject')


class Student(Base):
    __tablename__ = 'student'
    __table_args__ = {'comment': '学生表，属性包括\\r\\nid，\\r\\n姓名，\\r\\n手机号，\\r\\n邮箱，\\r\\n学生类型'}

    student_id = Column(String(16), primary_key=True)
    team_id = Column(ForeignKey('team.team_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True,
                     comment='初始为空')
    dept_id = Column(ForeignKey('dept.dept_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    password = Column(String(300), comment='哈希后的密文')
    phone_number = Column(String(16))
    email = Column(String(32))
    description = Column(Text)
    gender = Column(TINYINT(1))
    birthday = Column(Date)
    student_name = Column(String(16))
    student_type = Column(String(10), comment='硕士生、博士生')
    student_class = Column(String(10))
    resume = Column(LargeBinary)

    dept = relationship('Dept')
    team = relationship('Team')


# t_wish_list = Table(
#     'wish_list', metadata,
#     Column('subject_id', ForeignKey('subject.subject_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True),
#     Column('team_id', ForeignKey('team.team_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True),
#     Column('join_time', DateTime),
#     comment='愿望单'
# )


# 10.25 新建愿望单、申请表
# 愿望单
class WishList(Base):
    __tablename__ = 'wish_list'
    __table_args__ = {'comment': '愿望单'}
    subject_id = Column(ForeignKey('subject.subject_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True,
                        primary_key=True)
    team_id = Column(ForeignKey('team.team_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, primary_key=True)
    join_time = Column(DateTime)

    subject = relationship('Subject')
    team = relationship('Team')


# 申请选课表
class Apply2Select(Base):
    __tablename__ = 'apply_to_select'
    __table_args__ = {'comment': '申请选题'}

    team_id = Column(ForeignKey('team.team_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True,
                     primary_key=True)
    subject_id = Column(ForeignKey('subject.subject_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True,
                        primary_key=True)
    status = Column(String(16))
    version = Column(Integer)
    created_time = Column(DateTime)
    last_modified_time = Column(DateTime)
    subject = relationship('Subject')
    team = relationship('Team')


# 申请加入小组表
class Apply2Join(Base):
    __tablename__ = 'apply_to_join'
    __table_args__ = {'comment': '申请加入小组'}
    team_id = Column(ForeignKey('team.team_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True,
                     primary_key=True)
    # partipant_id
    participant_id = Column(ForeignKey('student.student_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True,
                            primary_key=True)
    status = Column(String(16))
    version = Column(Integer)
    created_time = Column(DateTime)
    last_modified_time = Column(DateTime)
    student = relationship('Student')
    team = relationship('Team')
