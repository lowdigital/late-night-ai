SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `tmp_late`
--

-- --------------------------------------------------------

--
-- Структура таблицы `topics_current`
--

CREATE TABLE `topics_current` (
  `id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `type` varchar(64) NOT NULL,
  `speaker` varchar(64) DEFAULT NULL,
  `priority` int(11) NOT NULL DEFAULT 0,
  `source` varchar(128) NOT NULL,
  `requestor_id` varchar(512) NOT NULL,
  `user_id` varchar(1024) DEFAULT NULL,
  `topic` varchar(2048) NOT NULL,
  `topic_original` varchar(2048) NOT NULL,
  `characters` text NOT NULL,
  `scenario` text NOT NULL,
  `npc` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `topics_generated`
--

CREATE TABLE `topics_generated` (
  `id` bigint(20) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `type` varchar(64) NOT NULL,
  `speaker` varchar(64) DEFAULT NULL,
  `priority` int(11) NOT NULL DEFAULT 0,
  `source` varchar(128) NOT NULL,
  `requestor_id` varchar(512) NOT NULL,
  `user_id` varchar(1024) DEFAULT NULL,
  `topic` varchar(2048) NOT NULL,
  `topic_original` varchar(2048) NOT NULL,
  `characters` text NOT NULL,
  `scenario` text NOT NULL,
  `npc` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `topics_suggested`
--

CREATE TABLE `topics_suggested` (
  `id` bigint(20) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `type` varchar(64) NOT NULL,
  `speaker` varchar(64) DEFAULT NULL,
  `url` varchar(2048) DEFAULT NULL,
  `priority` int(11) NOT NULL DEFAULT 0,
  `source` varchar(128) NOT NULL,
  `requestor_id` varchar(512) NOT NULL,
  `user_id` varchar(1024) DEFAULT NULL,
  `topic` varchar(2048) DEFAULT NULL,
  `topic_original` varchar(2048) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `topics_current`
--
ALTER TABLE `topics_current`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `topics_generated`
--
ALTER TABLE `topics_generated`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `topics_suggested`
--
ALTER TABLE `topics_suggested`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `topics_current`
--
ALTER TABLE `topics_current`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `topics_generated`
--
ALTER TABLE `topics_generated`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85848;

--
-- AUTO_INCREMENT для таблицы `topics_suggested`
--
ALTER TABLE `topics_suggested`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
