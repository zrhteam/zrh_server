// const path=require('path'); //调用node.js中的路径
// module.exports={
//     entry:{
//         index:'./src/js/index.js' //需要打包的文件
//     },
//     output:{
//         filename:'[name].js',    //输入的文件名是什么，生成的文件名也是什么
//         path:path.resolve(__dirname,'../out') //指定生成的文件目录
//     },
//     mode:"development"    //开发模式，没有对js等文件压缩，默认生成的是压缩文件
// }


var htmlWebpackPlugin = require('html-webpack-plugin');
var path = require('path');
module.exports = {
    entry:{
        index:'./src/js/index.js' //需要打包的文件
    },
    output: {
        path: path.resolve(__dirname, './dist/js'),
        filename: 'js/[name].bundle.js'
    },
    module: {
        loaders: [
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {importLoaders: 1} //这里可以简单理解为，如果css文件中有import 进来的文件也进行处理
                    },
                    {
                        loader: 'postcss-loader',
                        options: {           // 如果没有options这个选项将会报错 No PostCSS Config found
                            plugins: (loader) => [
                                require('postcss-import')({root: loader.resourcePath}),
                                require('autoprefixer')(), //CSS浏览器兼容
                                require('cssnano')()  //压缩css
                            ]
                        }
                    }
                ]
            }
        ]
    },

    plugins: [
        new htmlWebpackPlugin({
            filename: 'index.html',
            template: 'index.html',
            inject: 'body'     //将js文件插入body文件内
        }),
    ]
};