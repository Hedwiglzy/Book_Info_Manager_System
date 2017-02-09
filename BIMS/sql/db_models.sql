-- 数据库模型
-- 2017.02.09
-- by hedwig

-- 用户信息表
--
CREATE TABLE `BIMS_user` (
  `user_id`     INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `user_name`   VARCHAR(30)            NOT NULL,
  `password`    VARCHAR(30)            NOT NULL,
  `tel`         BIGINT                 NULL,
  `email`       VARCHAR(254)           NULL,
  `sex`         INTEGER                NULL,
  `birthday`    DATE                   NULL,
  `age`         INTEGER                NULL,
  `locate`      VARCHAR(50)            NULL,
  `remark`      VARCHAR(500)           NULL,
  `image`       VARCHAR(100)           NULL,
  `create_date` DATE                   NULL
)
  AUTO_INCREMENT = 10001;
--
-- 图书信息表
--
CREATE TABLE `BIMS_book` (
  `book_id`          INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `book_name`        VARCHAR(100)           NOT NULL,
  `author_name`      VARCHAR(100)           NOT NULL,
  `press_house`      VARCHAR(100)           NULL,
  `translator`       VARCHAR(100)           NULL,
  `publication_date` VARCHAR(100)           NULL,
  `pages`            INTEGER                NULL,
  `price`            INTEGER                NULL,
  `package`          VARCHAR(10)            NULL,
  `isbn`             BIGINT                 NULL,
  `score`            INTEGER                NULL,
  `evaluate_num`     INTEGER                NULL,
  `collect_num`      INTEGER                NULL,
  `content_summary`  LONGTEXT               NULL
)
  AUTO_INCREMENT = 10001;
--
-- 作者信息表
--
CREATE TABLE `BIMS_author` (
  `author_id`      INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `author_name`    VARCHAR(100)           NOT NULL,
  `nationality`    VARCHAR(100)           NULL,
  `author_summary` LONGTEXT               NULL
)
  AUTO_INCREMENT = 10001;
--
-- 收藏信息表
--
CREATE TABLE `BIMS_collection` (
  `op_id`       INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `user_name`   VARCHAR(30)            NOT NULL,
  `book_id`     INTEGER                NOT NULL,
  `book_name`   VARCHAR(100)           NOT NULL,
  `create_date` DATE                   NOT NULL
)
  AUTO_INCREMENT = 10001;


