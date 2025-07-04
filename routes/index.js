const express = require('express')
const router = express.Router()
const publicController = require('../controllers/publicController')

// 首页路由
router.get('/', publicController.renderHomePage)

// 课程中心页路由
router.get('/courses', publicController.renderCoursesPage)

// 课程详情页路由
router.get('/courses/:id', publicController.renderCourseDetailPage)

// 在线报名页面
router.get('/enroll/:courseId', publicController.renderEnrollPage)

// 处理报名表单提交
router.post('/enroll/:courseId', publicController.handleEnrollment)

// 师资力量页面
router.get('/teachers', publicController.renderTeachersPage)

// 关于我们页面
router.get('/about', publicController.renderAboutPage)

// 联系我们页面
router.get('/contact', publicController.renderContactPage)

module.exports = router
