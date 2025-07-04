const db = require('../db/connection')
const bcrypt = require('bcrypt')

// 渲染登录页面
exports.renderLoginPage = (req, res) => {
    const errorMessage = req.session.errorMessage
    req.session.errorMessage = null // 清除错误消息
    res.render('admin/login', {
        pageTitle: '管理员登录',
        errorMessage: errorMessage,
        isAdmin: true
    })
}

// 处理登录逻辑
exports.handleLogin = async (req, res) => {
    try {
        const { username, password } = req.body

        // 从数据库查找用户
        const [users] = await db.query('SELECT * FROM admins WHERE username = ?', [username])

        if (users.length === 0) {
            req.session.errorMessage = '用户名不存在'
            return res.redirect('/admin/login')
        }

        const user = users[0]

        // 验证密码
        const isPasswordValid = await bcrypt.compare(password, user.password)

        if (!isPasswordValid) {
            req.session.errorMessage = '密码错误'
            return res.redirect('/admin/login')
        }

        // 登录成功，保存用户信息到session（不包含密码）
        req.session.user = {
            id: user.id,
            username: user.username
        }

        res.redirect('/admin/dashboard')
    } catch (error) {
        console.error('登录过程中发生错误:', error)
        req.session.errorMessage = '登录过程中发生错误，请稍后重试'
        res.redirect('/admin/login')
    }
}

// 渲染后台管理主页
exports.renderDashboard = (req, res) => {
    res.render('admin/dashboard', {
        pageTitle: '管理后台',
        user: req.session.user,
        isAdmin: true,
        activePage: 'dashboard'
    })
}

// 渲染课程管理页面
exports.renderCoursesManagement = async (req, res) => {
    try {
        const [courses] = await db.query('SELECT * FROM courses ORDER BY created_at DESC')
        // 读取地图嵌入链接
        const [settings] = await db.query("SELECT * FROM site_settings WHERE setting_key = 'mapEmbedUrl'")
        const mapEmbedUrl = settings.length > 0 ? settings[0].setting_value : ''
        res.render('admin/courses', {
            pageTitle: '课程管理',
            user: req.session.user,
            courses: courses,
            mapEmbedUrl: mapEmbedUrl,
            isAdmin: true,
            activePage: 'courses'
        })
    } catch (error) {
        console.error('获取课程列表失败:', error)
        res.status(500).send('服务器错误')
    }
}

// 添加新课程
exports.addCourse = async (req, res) => {
    try {
        const { title, description, category, suitable_age, capacity } = req.body

        await db.query(
            'INSERT INTO courses (title, description, category, suitable_age, capacity) VALUES (?, ?, ?, ?, ?)',
            [title, description, category, suitable_age, capacity]
        )

        res.redirect('/admin/courses')
    } catch (error) {
        console.error('添加课程失败:', error)
        res.status(500).send('添加课程失败')
    }
}

// 删除课程
exports.deleteCourse = async (req, res) => {
    try {
        const courseId = req.params.id
        await db.query('DELETE FROM courses WHERE id = ?', [courseId])
        res.redirect('/admin/courses')
    } catch (error) {
        console.error('删除课程失败:', error)
        res.status(500).send('删除课程失败')
    }
}

// 处理登出逻辑
exports.handleLogout = (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            console.error('登出时发生错误:', err)
        }
        res.redirect('/admin/login')
    })
}

// 更新课程
exports.updateCourse = async (req, res) => {
    try {
        const courseId = req.params.id
        const { title, description, category, age_range, duration, class_size, price, content } = req.body

        await db.query(
            'UPDATE courses SET title = ?, description = ?, category = ?, age_range = ?, duration = ?, class_size = ?, price = ?, content = ? WHERE id = ?',
            [title, description, category, age_range, duration, class_size, price, content, courseId]
        )

        res.redirect('/admin/courses')
    } catch (error) {
        console.error('更新课程失败:', error)
        res.status(500).send('更新课程失败')
    }
}

// 渲染报名管理页面
exports.renderEnrollmentsManagement = async (req, res) => {
    try {
        const [enrollments] = await db.query(`
            SELECT 
                e.id, 
                e.student_name,
                e.student_age,
                e.parent_name,
                e.parent_phone, 
                e.status, 
                e.created_at, 
                e.notes, 
                c.title as course_title
            FROM enrollments e 
            LEFT JOIN courses c ON e.course_id = c.id 
            ORDER BY e.created_at DESC
        `)
        console.log('enrollments:', enrollments)
        res.render('admin/enrollments', {
            pageTitle: '报名管理',
            user: req.session.user,
            enrollments: enrollments,
            isAdmin: true,
            activePage: 'enrollments'
        })
    } catch (error) {
        console.error('获取报名列表失败:', error)
        res.status(500).send('服务器错误')
    }
}

// 更新报名状态
exports.updateEnrollmentStatus = async (req, res) => {
    try {
        const enrollmentId = req.params.id
        const { status, notes } = req.body

        await db.query(
            'UPDATE enrollments SET status = ?, notes = ?, updated_at = NOW() WHERE id = ?',
            [status, notes, enrollmentId]
        )

        res.redirect('/admin/enrollments')
    } catch (error) {
        console.error('更新报名状态失败:', error)
        res.status(500).send('更新报名状态失败')
    }
}

// 删除报名记录
exports.deleteEnrollment = async (req, res) => {
    try {
        const enrollmentId = req.params.id
        await db.query('DELETE FROM enrollments WHERE id = ?', [enrollmentId])
        res.redirect('/admin/enrollments')
    } catch (error) {
        console.error('删除报名记录失败:', error)
        res.status(500).send('删除报名记录失败')
    }
}

// 渲染教师管理页面
exports.renderTeachersManagement = async (req, res) => {
    try {
        const [teachers] = await db.query('SELECT * FROM teachers ORDER BY years_experience DESC')
        res.render('admin/teachers', {
            pageTitle: '教师管理',
            user: req.session.user,
            teachers: teachers,
            isAdmin: true,
            activePage: 'teachers'
        })
    } catch (error) {
        console.error('获取教师列表失败:', error)
        res.status(500).send('服务器错误')
    }
}

// 添加新教师
exports.addTeacher = async (req, res) => {
    try {
        const { name, title, education, years_experience, specialty, bio, phone, email, photo_url } = req.body
        let finalPhotoUrl = photo_url
        if (req.file) {
            finalPhotoUrl = '/uploads/' + req.file.filename
        }

        // 如果 years_experience 是空字符串或未定义，则将其设置为 null，否则转换为整数
        const final_years_experience = (years_experience === '' || years_experience === undefined) ? null : parseInt(years_experience, 10)

        await db.query(
            'INSERT INTO teachers (name, title, specialty, bio, photo_url, years_experience, education, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            [name, title, specialty, bio, finalPhotoUrl, final_years_experience, education, phone, email]
        )
        res.redirect('/admin/teachers')
    } catch (error) {
        console.error('添加教师失败:', error)
        res.status(500).send(`添加教师失败: ${error.sqlMessage || error.message}`)
    }
}

// 更新教师信息
exports.updateTeacher = async (req, res) => {
    try {
        const teacherId = req.params.id
        const { name, title, education, years_experience, specialty, bio, phone, email, photo_url } = req.body
        let finalPhotoUrl = photo_url
        if (req.file) {
            finalPhotoUrl = '/uploads/' + req.file.filename
        }

        // 如果 years_experience 是空字符串或未定义，则将其设置为 null，否则转换为整数
        const final_years_experience = (years_experience === '' || years_experience === undefined) ? null : parseInt(years_experience, 10)

        await db.query(
            'UPDATE teachers SET name = ?, title = ?, specialty = ?, bio = ?, photo_url = ?, years_experience = ?, education = ?, phone = ?, email = ? WHERE id = ?',
            [name, title, specialty, bio, finalPhotoUrl, final_years_experience, education, phone, email, teacherId]
        )

        res.redirect('/admin/teachers')
    } catch (error) {
        console.error('更新教师信息失败:', error)
        res.status(500).send(`更新教师信息失败: ${error.sqlMessage || error.message}`)
    }
}

// 删除教师
exports.deleteTeacher = async (req, res) => {
    try {
        const teacherId = req.params.id
        await db.query('DELETE FROM teachers WHERE id = ?', [teacherId])
        res.redirect('/admin/teachers')
    } catch (error) {
        console.error('删除教师失败:', error)
        res.status(500).send('删除教师失败')
    }
}

// 渲染网站设置页面
exports.renderSiteSettings = async (req, res) => {
    try {
        const [settings] = await db.query('SELECT * FROM site_settings')
        const settingsObj = {}
        settings.forEach(setting => {
            settingsObj[setting.setting_key] = setting.setting_value
        })
        // 兼容旧数据，若无mapEmbedUrl/home_video_url则补空字符串
        if (!('mapEmbedUrl' in settingsObj)) settingsObj.mapEmbedUrl = ''
        if (!('home_video_url' in settingsObj)) settingsObj.home_video_url = ''
        res.render('admin/settings', {
            pageTitle: '网站设置',
            user: req.session.user,
            settings: settingsObj,
            isAdmin: true,
            activePage: 'settings'
        })
    } catch (error) {
        console.error('获取网站设置失败:', error)
        res.status(500).send('服务器错误')
    }
}

// 更新网站设置
exports.updateSiteSettings = async (req, res) => {
    try {
        const settings = req.body

        for (const [key, value] of Object.entries(settings)) {
            await db.query(
                'INSERT INTO site_settings (setting_key, setting_value) VALUES (?, ?) ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value)',
                [key, value]
            )
        }

        res.redirect('/admin/settings')
    } catch (error) {
        console.error('更新网站设置失败:', error)
        res.status(500).send('更新网站设置失败')
    }
}

// 获取统计数据
exports.getDashboardStats = async (req, res) => {
    try {
        // 获取各种统计数据
        const [courseCount] = await db.query('SELECT COUNT(*) as count FROM courses')
        const [enrollmentCount] = await db.query('SELECT COUNT(*) as count FROM enrollments')
        const [teacherCount] = await db.query('SELECT COUNT(*) as count FROM teachers')
        const [pendingEnrollments] = await db.query('SELECT COUNT(*) as count FROM enrollments WHERE status = "pending"')

        // 最近的报名记录
        const [recentEnrollments] = await db.query(`
            SELECT e.*, c.title as course_title 
            FROM enrollments e 
            LEFT JOIN courses c ON e.course_id = c.id 
            ORDER BY e.created_at DESC 
            LIMIT 5
        `)

        const stats = {
            courses: courseCount[0].count,
            enrollments: enrollmentCount[0].count,
            teachers: teacherCount[0].count,
            pendingEnrollments: pendingEnrollments[0].count,
            recentEnrollments: recentEnrollments
        }

        res.json(stats)
    } catch (error) {
        console.error('获取统计数据失败:', error)
        res.status(500).json({ error: '获取统计数据失败' })
    }
}
