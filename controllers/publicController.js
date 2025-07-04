const db = require('../db/connection')

/**
 * 渲染首页
 */
exports.renderHomePage = async (req, res) => {
    try {
        // 读取首页视频链接
        const [rows] = await db.query("SELECT setting_value FROM site_settings WHERE setting_key = 'home_video_url' LIMIT 1")
        const homeVideoUrl = rows.length > 0 ? rows[0].setting_value : ''
        res.render('index', {
            pageTitle: '首页',
            homeVideoUrl: homeVideoUrl
        })
    } catch (error) {
        console.error("获取首页数据失败:", error)
        res.status(500).send("服务器错误")
    }
}

/**
 * 渲染课程中心页面
 * 1. 从数据库获取所有课程数据
 * 2. 将数据传递给 courses.ejs 模板进行渲染
 */
exports.renderCoursesPage = async (req, res) => {
    try {
        const [courses] = await db.query("SELECT * FROM courses ORDER BY created_at DESC")

        // 使用 res.render() 渲染页面
        res.render('courses', { // 'courses' 对应 views/courses.ejs 文件
            pageTitle: '课程中心', // 传递给模板的变量
            courses: courses       // 传递给模板的变量
        })
    } catch (error) {
        console.error("获取课程页面数据时发生严重错误:", error)
        res.status(500).send("服务器内部错误，请查看服务器日志了解详情。")
    }
}

/**
 * 渲染课程详情页面
 */
exports.renderCourseDetailPage = async (req, res) => {
    try {
        const courseId = req.params.id
        const [rows] = await db.query("SELECT * FROM courses WHERE id = ?", [courseId])

        if (rows.length === 0) {
            return res.status(404).render('course-detail', {
                pageTitle: '未找到课程',
                course: null
            })
        }

        const course = rows[0]

        res.render('course-detail', {
            pageTitle: course.title,
            course: course
        })
    } catch (error) {
        console.error("获取课程详情失败:", error)
        res.status(500).send("服务器错误")
    }
}

/**
 * 渲染师资力量页面
 */
exports.renderTeachersPage = (req, res) => {
    res.render('teachers', {
        pageTitle: '师资力量'
    })
}

/**
 * 渲染关于我们页面
 */
exports.renderAboutPage = (req, res) => {
    res.render('about', {
        pageTitle: '关于我们'
    })
}

/**
 * 渲染联系我们页面
 */
exports.renderContactPage = async (req, res) => {
    try {
        const [rows] = await db.query("SELECT setting_value FROM site_settings WHERE setting_key = 'mapEmbedUrl' LIMIT 1")
        const mapEmbedUrl = rows.length > 0 ? rows[0].setting_value : ''

        res.render('contact', {
            pageTitle: '联系我们',
            mapEmbedUrl: mapEmbedUrl
        })
    } catch (error) {
        console.error("获取联系我们页面数据失败:", error)
        res.status(500).send("服务器错误")
    }
}

/**
 * 渲染在线报名页面
 */
exports.renderEnrollPage = async (req, res) => {
    try {
        const courseId = req.params.courseId
        const [rows] = await db.query("SELECT * FROM courses WHERE id = ?", [courseId])

        if (rows.length === 0) {
            return res.status(404).send('课程不存在')
        }

        const course = rows[0]
        res.render('enroll', {
            pageTitle: '课程报名',
            course: course
        })
    } catch (error) {
        console.error("获取报名页面失败:", error)
        res.status(500).send("服务器错误")
    }
}

/**
 * 处理报名表单提交
 */
exports.handleEnrollment = async (req, res) => {
    try {
        const courseId = req.params.courseId
        const { student_name, student_age, parent_name, parent_phone, parent_email, notes } = req.body

        await db.query(
            'INSERT INTO enrollments (course_id, student_name, student_age, parent_name, parent_phone, parent_email, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
            [courseId, student_name, student_age, parent_name, parent_phone, parent_email, notes]
        )

        res.render('enroll-success', {
            pageTitle: '报名成功',
            message: '您的报名申请已提交成功！我们会在24小时内与您联系确认详情。'
        })
    } catch (error) {
        console.error("处理报名失败:", error)
        res.status(500).send('报名失败，请稍后重试')
    }
}

/**
 * 渲染师资力量页面（从数据库获取）
 */
exports.renderTeachersPage = async (req, res) => {
    try {
        const [teachers] = await db.query("SELECT * FROM teachers ORDER BY years_experience DESC")
        res.render('teachers', {
            pageTitle: '师资力量',
            teachers: teachers
        })
    } catch (error) {
        console.error("获取师资信息失败:", error)
        res.render('teachers', {
            pageTitle: '师资力量',
            teachers: []
        })
    }
}

/**
 * 渲染旅行页面
 */
exports.renderTravelPage = (req, res) => {
    res.render('travel', {
        pageTitle: '旅行探索'
    })
}
