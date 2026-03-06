# 全局安装（Dart Sass - 官方推荐）
npm install -g sass

# 项目本地安装
npm install --save-dev sass

# 检查版本
sass --version

# 查看帮助
sass --help

# 编译单个文件
sass input.scss output.css

# 编译并压缩输出
sass input.scss output.css --style compressed

1. 变量 (Variables)
// 定义变量
$primary-color: #3498db;
$font-stack: Helvetica, sans-serif;
$margin: 15px;
$base-padding: 10px !default; // 默认变量

// 使用变量
body {
  color: $primary-color;
  font-family: $font-stack;
}

2. 嵌套 (Nesting)
// 选择器嵌套
nav {
  ul {
    margin: 0;
    padding: 0;
    li {
      display: inline-block;
      a {
        text-decoration: none;
        &:hover { // & 引用父选择器
          color: red;
        }
      }
    }
  }
}

// 属性嵌套
.box {
  font: {
    family: Arial;
    size: 14px;
    weight: bold;
  }
  border: {
    top: 1px solid #ccc;
    left: 2px solid #ddd;
  }
}

3. 混合 (Mixins)
// 定义混合
@mixin border-radius($radius: 5px) {
  -webkit-border-radius: $radius;
  -moz-border-radius: $radius;
  border-radius: $radius;
}

@mixin flex-center($direction: row) {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: $direction;
}

// 使用混合
.button {
  @include border-radius(10px);
  @include flex-center(column);
}

// 传递内容块
@mixin hover-effect {
  &:hover {
    @content;
  }
}

.link {
  @include hover-effect {
    color: blue;
    text-decoration: underline;
  }
}

4. 继承 (Extend/Inheritance)
// 占位符选择器
%message-shared {
  border: 1px solid #ccc;
  padding: 10px;
  color: #333;
}

%clearfix {
  &::after {
    content: "";
    display: table;
    clear: both;
  }
}

// 继承
.message {
  @extend %message-shared;
}

.success {
  @extend %message-shared;
  border-color: green;
}

.container {
  @extend %clearfix;
}

5. 运算 (Operations)
$base-size: 16px;
$container-width: 960px;

.element {
  // 算术运算
  width: $container-width / 2 - 20px;
  font-size: $base-size * 1.5;
  padding: 10px + 5px;
  
  // 颜色运算
  color: #112233 + #445566;
  background-color: rgba(255, 0, 0, 0.75) * 0.5;
  
  // 字符串运算
  font-family: "Arial" + ", sans-serif";
  
  // 布尔运算
  $has-border: true;
  border: if($has-border, 1px solid #ccc, null);
}

6. 函数 (Functions)
// 内置函数
.element {
  color: lighten(#336699, 20%);
  background: darken(#ff0000, 15%);
  width: percentage(0.5);
  margin: round(3.4px);
  font-size: ceil(14.2px);
  
  // 透明度
  background: rgba(255, 0, 0, 0.5);
  background: transparentize(#ff0000, 0.3);
}

// 自定义函数
@function em($pixels, $context: 16px) {
  @return ($pixels / $context) * 1em;
}

@function color-shade($color, $percent) {
  @return mix(black, $color, $percent);
}

.element {
  font-size: em(24px); // 1.5em
  background: color-shade(#3498db, 20%);
}

