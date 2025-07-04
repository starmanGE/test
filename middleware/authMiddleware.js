// 检查用户是否登录的中间件
const isLoggedIn = (req, res, next) => {
    if (req.session && req.session.user) {
        // 用户已登录，继续执行
        next()
    } else {
        // 用户未登录，重定向到登录页
        res.redirect('/admin/login')
    }
}

module.exports = { isLoggedIn }