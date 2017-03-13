-- 数据库模型
-- 2017.02.09
-- by hedwig

-- 用户信息表 --
CREATE TABLE `BIMS_user` (
  `user_id`     INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `user_name`   VARCHAR(30)            NOT NULL,
  `password`    VARCHAR(30)            NOT NULL,
  `tel`         BIGINT                 NULL,
  `email`       VARCHAR(254)           NULL,
  `sex`         INTEGER                NULL,
  `birthday`    DATE                   NULL,
  `age`         INTEGER                NULL,
  `province`    VARCHAR(50)            NULL,
  `city`        VARCHAR(50)            NULL,
  `remark`      VARCHAR(500)           NULL,
  `image`       INTEGER                NULL,
  `create_date` DATE                   NULL
)
  AUTO_INCREMENT = 10001;

-- 图书信息表 --
CREATE TABLE bims_book
(
  `book_id `         INT(11) AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `book_name`        VARCHAR(100)           NOT NULL,
  `author_name`      VARCHAR(100)           NOT NULL,
  `press_house`      VARCHAR(100),
  `translator`       VARCHAR(100),
  `publication_date` VARCHAR(100),
  `pages`            VARCHAR(100),
  `price`            VARCHAR(100),
  `package`          VARCHAR(100),
  `isbn`             BIGINT(20),
  `evaluate_num`     INT(11),
  `collect_num`      INT(11),
  `content_summary`  LONGTEXT,
  `title`            VARCHAR(100),
  `create_date`      DATE,
  `author_id`        INT(11)
)
  AUTO_INCREMENT = 10001;

-- 作者信息表 --
CREATE TABLE `BIMS_author` (
  `author_id`      INTEGER      NOT NULL PRIMARY KEY,
  `author_name`    VARCHAR(100) NOT NULL,
  `nationality`    VARCHAR(100) NULL,
  `author_summary` LONGTEXT     NULL
);

-- 图书收藏信息表 --
CREATE TABLE `BIMS_collectionbook` (
  `op_id`       INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `user_id`     INTEGER                NOT NULL,
  `book_id`     INTEGER                NOT NULL,
  `create_date` DATE                   NOT NULL
)
  AUTO_INCREMENT = 10001;

-- 作者收藏信息表 --
CREATE TABLE `BIMS_collectionauthor` (
  `op_id`       INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `user_id`     INTEGER                NOT NULL,
  `author_id`   INTEGER                NOT NULL,
  `create_date` DATE                   NOT NULL
)
  AUTO_INCREMENT = 10001;

-- 读书笔记信息表 --
CREATE TABLE `BIMS_booknote` (
  `note_id`     INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `book_id`     INTEGER                NOT NULL,
  `user_id`     INTEGER                NOT NULL,
  `user_name`   VARCHAR(100)           NOT NULL,
  `title`       VARCHAR(100)           NULL,
  `content`     LONGTEXT               NULL,
  `create_date` DATE                   NOT NULL
)
  AUTO_INCREMENT = 10001;

-- 图书评论表 --
CREATE TABLE `BIMS_bookevaluate` (
  `op_id`       INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `book_id`     INTEGER                NOT NULL,
  `user_name`   VARCHAR(100)           NOT NULL,
  `content`     LONGTEXT               NULL,
  `create_date` DATE                   NOT NULL
)
  AUTO_INCREMENT = 10001;

-- 图书评分表 --
CREATE TABLE `BIMS_bookscore` (
  `op_id`       INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `book_id`     INTEGER                NOT NULL,
  `user_id`     INTEGER                NOT NULL,
  `score`       DECIMAL(10, 1)         NOT NULL,
  `create_date` DATE                   NOT NULL
)
  AUTO_INCREMENT = 10001;

-- 图书链接表 --
CREATE TABLE all_book
(
  book_id    INT(11) PRIMARY KEY NOT NULL,
  book_class VARCHAR(100),
  book_name  VARCHAR(500),
  book_url   VARCHAR(100)
);


