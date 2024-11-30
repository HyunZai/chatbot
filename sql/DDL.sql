DROP TABLE IF EXISTS chat_messages;
DROP TABLE IF EXISTS chat_list;

CREATE TABLE `chat_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `chat_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `list_id` int NOT NULL,
  `user_message` text NOT NULL,  -- 사용자 메시지
  `bot_response` text NOT NULL,  -- 봇의 응답
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_list_id` (`list_id`),
  CONSTRAINT `fk_list_id` FOREIGN KEY (`list_id`) REFERENCES `chat_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);