# An Ant target for compressing JavaScript and CSS files #
This is an [Ant](http://ant.apache.org/) target with which you can minify (compress) JavaScript and CSS files in a specified directory recursively.

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
4. If the minified version already exists, it won't be overwritten
5. By default, ignore the JavaScript and CSS files in both **node_modules** and **bower_components**

## Vendors ##

1. [Google Closure Compiler](https://github.com/google/closure-compiler):
    - Version:        v20150126
    - Release date:   2015-01-27
    - License:        [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
2. [Yahoo YUI Compressor](http://yui.github.io/yuicompressor/):
	- Version:        2.4.7 (v2.4.8 has an issue on windows, see [Unable to specify absolute path for output file](https://github.com/yui/yuicompressor/issues/78))
    - Release date:   2013-05-15
    - License:        BSD

## License ##
MIT
