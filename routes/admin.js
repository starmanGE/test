const express = require('express')
const router = express.Router()
const adminController = require('../controllers/adminController')
const { isLoggedIn } = require('../middleware/authMiddleware')
const upload = require('../middleware/upload')

// 显示登录页面的路由
router.get('/login', adminController.renderLoginPage)

// 处理登录表单提交的路由
router.post('/login', adminController.handleLogin)

// 后台管理主页 (仪表盘)，受登录保护
router.get('/dashboard', isLoggedIn, adminController.renderDashboard)

// 获取仪表盘统计数据API
router.get('/api/dashboard-stats', isLoggedIn, adminController.getDashboardStats)

// 课程管理路由
router.get('/courses', isLoggedIn, adminController.renderCoursesManagement)
router.post('/courses', isLoggedIn, adminController.addCourse)
router.post('/courses/:id/update', isLoggedIn, adminController.updateCourse)
router.post('/courses/:id/delete', isLoggedIn, adminController.deleteCourse)

// 报名管理路由
router.get('/enrollments', isLoggedIn, adminController.renderEnrollmentsManagement)
router.post('/enrollments/:id/update-status', isLoggedIn, adminController.updateEnrollmentStatus)
router.post('/enrollments/:id/delete', isLoggedIn, adminController.deleteEnrollment)

// 教师管理路由
router.get('/teachers', isLoggedIn, adminController.renderTeachersManagement)
router.post('/teachers', isLoggedIn, upload.single('photo'), adminController.addTeacher)
router.put('/teachers/:id', isLoggedIn, upload.single('photo'), adminController.updateTeacher)
router.delete('/teachers/:id', isLoggedIn, adminController.deleteTeacher)

// 网站设置路由
router.get('/settings', isLoggedIn, adminController.renderSiteSettings)
router.post('/settings', isLoggedIn, adminController.updateSiteSettings)

// 登出路由
router.get('/logout', adminController.handleLogout)

module.exports = router