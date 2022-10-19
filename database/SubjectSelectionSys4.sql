/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2022/10/16 15:10:28                          */
/*==============================================================*/
DROP DATABASE IF EXISTS subject_selection_db;

CREATE DATABASE  IF NOT EXISTS subject_selection_db;
USE subject_selection_db;


DROP TABLE IF EXISTS dept;

DROP TABLE IF EXISTS instructor;

DROP TABLE IF EXISTS message;

DROP TABLE IF EXISTS release_subject;

DROP TABLE IF EXISTS student;

DROP TABLE IF EXISTS SUBJECT;

DROP TABLE IF EXISTS team;

DROP TABLE IF EXISTS wish_list;

/*==============================================================*/
/* Table: dept                                                  */
/*==============================================================*/
CREATE TABLE dept
(
   dept_id              BIGINT NOT NULL,
   dept_name            VARCHAR(8) COMMENT '软件学院',
   city                 VARCHAR(4) COMMENT '合肥、苏州',
   PRIMARY KEY (dept_id)
);

ALTER TABLE dept COMMENT '导师和学生所属院系
varchar长度按照 字长度计算';

/*==============================================================*/
/* Table: instructor                                            */
/*==============================================================*/
CREATE TABLE instructor
(
   instructor_id        VARCHAR(16) NOT NULL,
   dept_id              BIGINT,
   PASSWORD             VARCHAR(300) COMMENT '哈希后的密文',
   phone_number         VARCHAR(16),
   email                VARCHAR(32),
   DESCRIPTION          TEXT,
   gender               BOOL,
   birthday             date,
   instructor_name      varchar(16),
   title                varchar(8),
   primary key (instructor_id)
);

alter table instructor comment '指导教师，负责发布选题和确认小组选题情况。
属性包括：
id，
导师姓名，
                               -&#';

/*==============================================================*/
/* Table: message                                               */
/*==============================================================*/
create table message
(
   message_id           bigint not null,
   from_user            varchar(16),
   to_user              varchar(16),
   title                varchar(100),
   content              text,
   primary key (message_id)
);

alter table message comment '消息表';

/*==============================================================*/
/* Table: release_subject                                       */
/*==============================================================*/
create table release_subject
(
   instructor_id        varchar(16) not null,
   subject_id           bigint not null,
   released             bool comment '可以存为草稿',
   version              bigint,
   primary key (instructor_id, subject_id)
);

alter table release_subject comment '一个导师可以发布多个题目。
也可以有多个导师联合指导题目';

/*==============================================================*/
/* Table: student                                               */
/*==============================================================*/
create table student
(
   student_id           varchar(16) not null,
   team_id              bigint comment '初始为空',
   dept_id              bigint,
   password             varchar(300) comment '哈希后的密文',
   phone_number         varchar(16),
   email                varchar(32),
   description          text,
   gender               bool,
   birthday             date,
   student_name         varchar(16),
   student_type         varchar(10) comment '硕士生、博士生',
   student_class        varchar(10),
   resume               blob,
   primary key (student_id)
);

alter table student comment '学生表，属性包括
id，
姓名，
手机号，
邮箱，
学生类型';

/*==============================================================*/
/* Table: subject                                               */
/*==============================================================*/
create table subject
(
   subject_id           bigint not null,
   subject_name         varchar(30) not null,
   description          text,
   language             varchar(30),
   platform             varchar(30),
   min_person           int,
   max_person           int,
   innovation           varchar(10),
   max_group            int,
   origin               varchar(10) comment '企业课题、导师课题',
   created_time         datetime,
   last_modified_time   datetime,
   version              bigint,
   primary key (subject_id)
);

alter table subject comment '工程实践题目表。属性有：
id，
题目名称，
题目介绍，
题目来源（企业';

/*==============================================================*/
/* Table: team                                                  */
/*==============================================================*/
create table team
(
   team_id              bigint not null,
   subject_id           bigint,
   team_name            varchar(20),
   leader_id            varchar(16),
   version              bigint comment '每次加入/删除队员会更改版本号',
   primary key (team_id)
);

alter table team comment '小组';

/*==============================================================*/
/* Table: wish_list                                             */
/*==============================================================*/
create table wish_list
(
   subject_id           bigint,
   team_id              bigint,
   join_time            datetime
);

alter table wish_list comment '愿望单';

alter table instructor add constraint FK_Reference_5 foreign key (dept_id)
      references dept (dept_id) on delete restrict on update restrict;

alter table release_subject add constraint FK_release foreign key (instructor_id)
      references instructor (instructor_id) on delete restrict on update restrict;

alter table release_subject add constraint FK_release2 foreign key (subject_id)
      references subject (subject_id) on delete restrict on update restrict;

alter table student add constraint FK_Reference_6 foreign key (dept_id)
      references dept (dept_id) on delete restrict on update restrict;

alter table student add constraint FK_compose foreign key (team_id)
      references team (team_id) on delete restrict on update restrict;

alter table team add constraint FK_select foreign key (subject_id)
      references subject (subject_id) on delete restrict on update restrict;

alter table wish_list add constraint FK_Reference_7 foreign key (subject_id)
      references subject (subject_id) on delete restrict on update restrict;

alter table wish_list add constraint FK_Reference_8 foreign key (team_id)
      references team (team_id) on delete restrict on update restrict;

