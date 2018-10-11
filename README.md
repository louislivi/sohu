# sohu
## 爬去搜狐文章分类 文章列表以及文章内容

## db name:
 *  news

## tables name:
 * article

```
-- auto-generated definition
create table article
(
id          int(11) unsigned                    not null
  primary key,
author_id   int(11) unsigned                    not null,
author_pic  varchar(500)                        not null,
author_name varchar(50)                         not null,
title       varchar(200)                        not null,
picurl      varchar(500)                        not null,
images      text                                not null,
public_time int                                 not null,
cms_id      int                                 not null,
reading     int(11) unsigned default '0'        not null,
type        int                                 not null,
create_time timestamp default CURRENT_TIMESTAMP not null,
update_time timestamp default CURRENT_TIMESTAMP not null,
source      int(50) default '1'                 not null
comment '出处',
articleid   int auto_increment,
constraint articleid
unique (articleid)
)
engine = InnoDB;

create index fulltext_article
on article (title, author_name);


```

* article_content

```
-- auto-generated definition
create table article_content
(
article_id int(11) unsigned not null
  primary key,
content    longtext         not null
)
engine = InnoDB;

create index fulltext_article
on article_content (content);
```

* type

```
-- auto-generated definition
create table type
(
id   int auto_increment
  primary key,
No   int          null
comment '编号',
name varchar(255) null
comment '名称',
sort int          null
)
engine = InnoDB;
INSERT INTO news.type (id, No, name, sort) VALUES (1, 8, '新闻', 2);
INSERT INTO news.type (id, No, name, sort) VALUES (2, 15, '财经', 3);
INSERT INTO news.type (id, No, name, sort) VALUES (3, 10, '军事', 6);
INSERT INTO news.type (id, No, name, sort) VALUES (4, 23, '时尚', 13);
INSERT INTO news.type (id, No, name, sort) VALUES (5, 13, '历史', 9);
INSERT INTO news.type (id, No, name, sort) VALUES (6, 30, '科技', 10);
INSERT INTO news.type (id, No, name, sort) VALUES (7, 25, '教育', 11);
INSERT INTO news.type (id, No, name, sort) VALUES (8, 24, '健康', 7);
INSERT INTO news.type (id, No, name, sort) VALUES (9, 26, '母婴', 12);
INSERT INTO news.type (id, No, name, sort) VALUES (10, 12, '文化', 14);
INSERT INTO news.type (id, No, name, sort) VALUES (11, 43, '社会', 15);
INSERT INTO news.type (id, No, name, sort) VALUES (12, 42, '游戏', 16);
INSERT INTO news.type (id, No, name, sort) VALUES (13, 41, '动漫', 17);
INSERT INTO news.type (id, No, name, sort) VALUES (14, 29, '旅游', 18);
INSERT INTO news.type (id, No, name, sort) VALUES (15, 28, '美食', 19);
INSERT INTO news.type (id, No, name, sort) VALUES (16, 27, '星座', 20);
INSERT INTO news.type (id, No, name, sort) VALUES (17, 45, '搞笑', 21);
INSERT INTO news.type (id, No, name, sort) VALUES (18, 44, '宠物', 22);
INSERT INTO news.type (id, No, name, sort) VALUES (19, 17, '体育', 4);
INSERT INTO news.type (id, No, name, sort) VALUES (20, 18, '汽车', 8);
INSERT INTO news.type (id, No, name, sort) VALUES (21, 19, '娱乐', 5);
INSERT INTO news.type (id, No, name, sort) VALUES (22, 1, '推荐', 1);
```
