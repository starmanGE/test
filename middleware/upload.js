const multer = require('multer')
const path = require('path')

// 设置存储路径和文件名
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, path.join(__dirname, '../public/uploads'))
    },
    filename: function (req, file, cb) {
        const ext = path.extname(file.originalname)
        const basename = path.basename(file.originalname, ext)
        cb(null, basename + '-' + Date.now() + ext)
    }
})

const upload = multer({ storage })

module.exports = upload
