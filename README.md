<!--
 * @Description: 
 * @Author: cc
 * @Date: 2021-04-28 10:30:20
 * @LastEditors: cc
 * @LastEditTime: 2021-04-29 18:21:42
-->
# Snoval

![GitHub](https://img.shields.io/github/license/needhourger/snovel)
![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/needhourger/snovel?include_prereleases)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/needhourger/snovel)

Shell novel 一个可以在命令行看小说的小工具

使用纯python语言编写


## Table of Contents

- [Snoval](#snoval)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Install](#install)
  - [Usage](#usage)
  - [Change Log](#change-log)
    - [Project Planning](#project-planning)
    - [v0.1.2 (2021/4/29)](#v012-2021429)
    - [v0.1.1 (2021/4/29)](#v011-2021429)
    - [v0.1.0 (2021/4/28)](#v010-2021428)
  - [License](#license)

## Background

一个简单的个人练手项目,以及为了能够实现在某些条件下摸鱼的小工具,当然目前还有很多功能尚未完善,未完待续...

## Install
```
pip install -r reqirements.txt
```

## Usage
1. 基本使用方法:
```
usage: snovel.py [-h] [-a ADD [ADD ...]] [-l] [-d DELETE [DELETE ...]]

A python based shell text novel reader

optional arguments:
-h, --help            show this help message and exit
-a ADD [ADD ...], --add ADD [ADD ...] 
                      add book to shelf;eg. --add ./test1.txt
-l, --list            list books
-d DELETE [DELETE ...], --delete DELETE [DELETE ...]
                      delete book by id;eg. --delete 1 2 3
```

2. 浏览书架书籍
```
$ python snovel.py -l
[id]: 1  [path]: D:\snovel\test.txt
[id]: 2  [path]: D:\snovel\test1.txt
[id]: 3  [path]: D:\snovel\test3.txt
[id]: 4  [path]: D:\snovel\test4.txt
```
1. 添加书籍
```
$ python snovel.py -a ./
[add book]: D:\snovel\test.txt]
[add book]: D:\snovel\test1.txt]
[add book]: D:\snovel\test3.txt]
[add book]: D:\snovel\test4.txt]
```

1. 删除书籍
```
$ python snovel.py -d 1 2 3 4 5
```
1. 阅读书籍
```
$ python snovel.py
```
1. 使用tab切换焦点,使用方向键选择图书,章节

2. 使用回车或者空格选定特定的书籍章节
   
3. 使用Ctrl+x载入指定图书章节
   
4. 使用ctrl+right向后翻页,ctrl+left向前翻页
   
5. 使用ctrl+c退出程序

## Change Log

### Project Planning
- [x] 实现记录阅读进度
- [x] 双向翻页
- [x] 优化单页显示
- [ ] 自动打开上次阅读书籍

### v0.1.2 (2021/4/29)

- 实现阅读进度自动保存
- 数据存储使用sqlite数据库

### v0.1.1 (2021/4/29)

- 实现双向翻页
- 修正单页数据显示错乱

### v0.1.0 (2021/4/28)

- 初次上传
- 基本的图书展示,翻页功能

## License

![GitHub](https://img.shields.io/github/license/needhourger/snovel)

