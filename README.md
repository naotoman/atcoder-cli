# Cli tools for AtCoder
Just another CLI tool for AtCoder contests.

## Requirements
- macOS or Linux
- Python >= 3.6

## How to install
```
$ python3 -m pip install git+https://github.com/naotoman/atcoder-cli
```

## How to use
For example, you want to join ABC140 with python3.  

### Quickstart
The most basic way to use this tool is the following.  

__1. Initiation__  
Type this command.  
```
$ atc gen abc140 -l python
```  
This makes directories and files under the current directory for the contest.  
__2. Write your code__  
Write your code on the files generated in step 1.  
For example, write your code for problem A on `./abc140/python/src/a.py`.  
__3. Submit your code__  
If you want to submit your code, then type this command.  
(Problem A, as an example)  
```
$ atc sub a
```  
This command does two things. First, it tests your code with the sample inputs on AtCoder Custom Test Server. Then, if the all tests are passed, it submits your code.

### Advanced
Once you run the command `atc gen`, conf.json is created under the path `$HOME/.atcoder_cli_info`.  
You can edit this file so that you can use this tool without running `atc gen` command. You can specify the paths to your source codes on conf.json.

### Others
Further explanation will be added in the future.  
For now, type this command.  
```
$ atc --help
```
