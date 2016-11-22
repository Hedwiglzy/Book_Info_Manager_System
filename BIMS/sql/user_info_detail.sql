CREATE TABLE `BIMS_user`
(
  `user_id`   bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `user_name` varchar(30)             NOT NULL,
  `password`  varchar(30)             NOT NULL,
  `tel`       bigint                  NULL,
  `email`     varchar(254)            NULL,
  `sex`       integer                 NULL,
  `birthday`  date                    NULL,
  `age`       integer                 NULL,
  `locate`    varchar(50)             NULL,
  `remark`    varchar(500)            NULL,
  `image`     varchar(100)            NULL
)AUTO_INCREMENT = 10001;
COMMIT;

