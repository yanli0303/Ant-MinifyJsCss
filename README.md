# Ant-MinifyJsCss

[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE.md)
[![PayPayl donate button](http://img.shields.io/badge/paypal-donate-orange.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=silentwait4u%40gmail%2ecom&lc=US&item_name=Yan%20Li&no_note=0&currency_code=USD&bn=PP%2dDonationsBF%3apaypal%2ddonate%2ejpg%3aNonHostedGuest)

This is an [Apache Ant](https://ant.apache.org/) project with which you can minify (compress) JavaScript and CSS files in a specified directory recursively.

## Usage ##
    ant -Dsrc="Home directory of your source files" minify

## Note ##

1. Extension of CSS files should be **.css**
    - Extension of minified CSS files will be **.min.css**
    - CSS files will be minified with [YUI Compressor](http://yui.github.io/yuicompressor/)
2. Extension of JavaScript files should be **.js**
    - Extension of minified JavaScript files will be **.min.js**
    - JavaScript files will be minified with [Google Closure Compiler](https://github.com/google/closure-compiler)
3. The minified files will be put in the same directory of unminified file
4. If the minified version already exists, it will be overwritten
5. By default, ignore the JavaScript and CSS files in directories named:
    - node_modules
    - bower_components
    - assets
    - yii
    - protected/runtime
    - protected/tests
6. If you have a [multi-core processor](https://en.wikipedia.org/wiki/Multi-core_processor), your JavaScript and CSS files will be minified concurrently

## Vendors ##

1. [Google Closure Compiler](https://github.com/google/closure-compiler):
    - Version:        v20150901
    - Release date:   2015-09-02
    - License:        [Apache License 2.0](https://github.com/google/closure-compiler#closure-compiler-license)
2. [Yahoo YUI Compressor](http://yui.github.io/yuicompressor/):
    - Version:        2.4.7 (v2.4.8 has an issue on windows, see [Unable to specify absolute path for output file](https://github.com/yui/yuicompressor/issues/78))
    - Release date:   2013-05-15
    - License:        [BSD](https://github.com/yui/yuicompressor/blob/master/LICENSE.TXT)
3. [ANT Contrib](http://ant-contrib.sourceforge.net/)
    - Version:        1.0b3
    - Release date:   2006-11-02
    - License:        [Apache Software License, Version 1.1](lib/ant-contrib/docs/LICENSE.txt)
    - This product includes software developed by the Ant-Contrib project (http://sourceforge.net/projects/ant-contrib).
