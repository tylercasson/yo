# yo, a command runner

`yo` is a useful command-line utility for aliasing and running otherwise long commands.

## Installation

```
git clone https://github.com/tylercasson/yo
cd yo
python3 setup.py install --user
```

Note that installation may vary on each system. This should work assuming your `PATH` is configured appropriately

## Usage

```
$ yo help
usage: yo [-h] [-g]
          {help,init,destroy,wipe,add,remove,rm,rename,mv,run,list,ls,edit}
          ...

Yo command runner

optional arguments:
  -h, --help            show this help message and exit
  -g, --global          use global config

commands:
    help                show this help message and exit
    init                initialize command file
    destroy (wipe)      remove command file
    add                 add command
    remove (rm)         remove command
    rename (mv)         rename command
    run                 run command
    list (ls)           list available command
    edit                edit configuration
```

### Initialize configuration

```
$ yo init
```

### Add commands

```
$ yo add <alias> "<command>"

# Example
$ yo add docker:clean "docker images -f dangling=true --quiet | xargs --no-run-if-empty docker rmi"
```

### Run commands

```
$ yo run <alias>

# Example
$ yo run docker:clean
```

### List available commands

```
$ yo list
```
