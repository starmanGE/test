// 引入必要的模块
const express = require('express')
const path = require('path')
const dotenv = require('dotenv')
const session = require('express-session')
const methodOverride = require('method-override')

// 加载环境变量
dotenv.config()

const app = express()
const PORT = process.env.PORT || 3000

// 1. 设置模板引擎为 EJS
app.set('view engine', 'ejs')
// 2. 指定模板文件的存放目录
app.set('views', path.join(__dirname, 'views'))

// 3. 设置静态资源目录 (CSS, 前端JS, 图片)
// 浏览器可以直接访问 /css/style.css
app.use(express.static(path.join(__dirname, 'public')))

// Session 中间件配置
app.use(session({
    secret: 'a-very-strong-and-secret-key', // 强烈建议您在.env文件中设置一个更复杂的密钥
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false } // 如果使用HTTPS，请设置为 true
}))

// 用于解析POST请求的表单数据
app.use(express.urlencoded({ extended: true }))
app.use(express.json())

// Method Override 中间件，用于支持PUT和DELETE等HTTP方法
app.use(methodOverride('_method'))

// 引入路由文件
const publicRoutes = require('./routes/index')
const adminRoutes = require('./routes/admin')

// 使用路由
app.use('/', publicRoutes)
app.use('/admin', adminRoutes)

// 启动服务器
app.listen(PORT, () => {
    console.log(`服务器正在 http://localhost:${PORT} 运行`)
})
