# yo

yo command runner

# usage

```bash
# initialize configuration
yo init

# check usage
yo help

# add commands
yo add docker:clean "docker images -f dangling=true --quiet | xargs --no-run-if-empty docker rmi"

# and run it
yo run docker:clean

# list available commands
yo list
```
