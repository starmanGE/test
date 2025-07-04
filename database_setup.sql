USE my_project;

-- 管理员表
CREATE TABLE `admins` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(255) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL
);

-- 课程表
CREATE TABLE `courses` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `category` ENUM('物理', '化学', '生物') NOT NULL,
  `cover_image_url` VARCHAR(255),
  `suitable_age` VARCHAR(100),
  `capacity` INT DEFAULT 20,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 公司信息表
CREATE TABLE `company_info` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `about_us` TEXT,
  `contact_phone` VARCHAR(100),
  `address` VARCHAR(255)
);

-- 报名表
CREATE TABLE `enrollments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `course_id` INT NOT NULL,
  `student_name` VARCHAR(100) NOT NULL,
  `student_age` INT NOT NULL,
  `parent_name` VARCHAR(100) NOT NULL,
  `parent_phone` VARCHAR(20) NOT NULL,
  `parent_email` VARCHAR(100),
  `status` ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
  `enrollment_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `notes` TEXT,
  FOREIGN KEY (`course_id`) REFERENCES `courses`(`id`) ON DELETE CASCADE
);

-- 师资表
CREATE TABLE `teachers` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `title` VARCHAR(100) NOT NULL,
  `specialty` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `photo_url` VARCHAR(255),
  `years_experience` INT,
  `education` VARCHAR(255),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 网站设置表
CREATE TABLE `site_settings` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `setting_key` VARCHAR(100) NOT NULL UNIQUE,
  `setting_value` TEXT,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入一些示例数据
INSERT INTO `admins` (`username`, `password`) VALUES ('admin', 'password'); -- 在生产环境中请使用加密密码
INSERT INTO `courses` (`title`, `description`, `category`, `suitable_age`) VALUES ('神奇的物理世界', '探索力的奥秘', '物理', '8-10岁');

-- 插入一些示例师资数据
INSERT INTO `teachers` (`name`, `title`, `specialty`, `description`, `years_experience`, `education`) VALUES 
('张老师', '物理实验专家', '物理', '拥有10年小学科学教育经验，擅长将复杂的物理原理用有趣的实验展现给孩子们。', 10, '物理学硕士'),
('李老师', '化学实验专家', '化学', '化学专业硕士学位，8年教学经验，特别擅长安全有趣的化学实验设计。', 8, '化学专业硕士'),
('王老师', '生物实验专家', '生物', '生物学博士，专注于启发式教学，让孩子们在观察中发现生命的奥秘。', 12, '生物学博士'),
('陈老师', '综合科学导师', '综合科学', '拥有丰富的跨学科教学经验，善于将物理、化学、生物知识融合教学。', 15, '教育学硕士');

-- 插入网站基本设置
INSERT INTO `site_settings` (`setting_key`, `setting_value`) VALUES 
('about_us', '我们致力于通过有趣、安全的科学实验，激发小学生对科学的兴趣和好奇心，培养他们的科学思维和动手能力。'),
('contact_phone', '010-12345678'),
('contact_address', '北京市朝阳区科学大道123号 科学教育中心3楼'),
('contact_email', 'info@science-lab.com'),
('business_hours', '周一至周五：15:00-19:00，周六至周日：09:00-17:00');
