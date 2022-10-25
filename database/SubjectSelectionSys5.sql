/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2022/10/24 10:47:34                          */
/*==============================================================*/


drop table if exists apply_to_join;

drop table if exists apply_to_select;


/*==============================================================*/
/* Table: apply_to_join                                         */
/*==============================================================*/
create table apply_to_join
(
   team_id              bigint,
   participant_id         varchar(16),
   status               varchar(16),
   version              int,
   created_time         datetime,
   last_modified_time   datetime
);

alter table apply_to_join comment '申请加入小组';

/*==============================================================*/
/* Table: apply_to_select                                       */
/*==============================================================*/
create table apply_to_select
(
   team_id              bigint,
   subject_id           bigint,
   status               varchar(16),
   version              int,
   created_time         datetime,
   last_modified_time   datetime
);

alter table apply_to_select comment '申请选题';


alter table apply_to_join add constraint FK_Reference_9 foreign key (team_id)
      references team (team_id) on delete restrict on update restrict;

alter table apply_to_join add constraint FK_申请加入小组 foreign key (participant_id)
      references student (student_id) on delete restrict on update restrict;

alter table apply_to_select add constraint FK_Reference_11 foreign key (team_id)
      references team (team_id) on delete restrict on update restrict;

alter table apply_to_select add constraint FK_Reference_12 foreign key (subject_id)
      references subject (subject_id) on delete restrict on update restrict;



