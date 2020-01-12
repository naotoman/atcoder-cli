# CLI for AtCoder
Just another CLI tool for AtCoder contests.

## Requirements
- macOS or Linux
- Python >= 3.6

## How to install
```sh
$ python3 -m pip install git+https://github.com/naotoman/atcoder-cli
```

## How to use
For example, Let's join ABC140 with python3.  

### Quickstart
The most basic way to use this tool is the following.  

__1. Init__  
Type this command.  
```sh
$ atc gen abc140 -l python
```  
This makes some directories and files for the contest under the current directory.  

__2. Write your code__  
Write your code on the files generated in step 1.  
For example, write your code for problem A on `./abc140/python/src/a.py`.  

__3. Submit your code__  
If you want to submit your code, then type this command.  
(Problem A, as an example)  
```sh
$ atc sub a
```  
This command does two things. First, it tests your code with the sample inputs on AtCoder Custom Test Server. Then, if the all tests are passed, it submits your code.

__4. See results of your submissions__  
If you want to know the results of your submissions, type this command.
```sh
$ atc result
```
This shows the results of the newest submission for each problem and also tells if you have ever gotten AC or not.

### Advanced
#### Without `atc gen`
If you have your own directory structure for the contests, You don't need to run `atc gen`.  
Instead, edit the file `$HOME/.atcoder_cli_info/conf.json`.  
This is an example of conf.json.  
```json:conf.json
{
    "contest": "abc149",
    "lang": "python",
    "src": {
        "a": "/Users/naoto/atcoder/contest/abc/abc_149/a.py",
        "b": "/Users/naoto/atcoder/contest/abc/abc_149/b.py",
        "c": "/Users/naoto/atcoder/contest/abc/abc_149/c.py",
        "d": "/Users/naoto/atcoder/contest/abc/abc_149/d.py",
        "e": "/Users/naoto/atcoder/contest/abc/abc_149/e.py",
        "f": "/Users/naoto/atcoder/contest/abc/abc_149/f.py"
    }
}
```
You can edit the values of "contest", "lang", and "src".  
"contest": The contest to join. te value is XXX for the url `https://atcoder.jp/contests/XXX`.  
"lang"   : The programming language for your code.  
"src"    : The object whose key is the problem and value is the path to your source code file for the problem.

### Languages
This tool can handle following languages.

|Name|AtCoder official name|
|:-----|:--------------------|
|python|Python3 (3.4.3)|
|pypy|PyPy3 (2.4.0)|
|rust|Rust (1.15.1)|
|kotlin|Kotlin (1.0.0)|
|cpp|C++14 (GCC 5.4.1)|
|java|Java8 (OpenJDK 1.8.0)|
