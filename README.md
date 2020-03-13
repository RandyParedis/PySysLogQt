# PySysLogQt
Simple `syslog` viewer written in `Python 3`.

**Note: It is nothing too fancy at this point in time. Currently, there are
no intentions of making this too fancy. Features may be requested in the
_Issues_ page.**

## Execution
### Run from Source
Make sure you have `Python 3` and `PyQt5` installed.
In the root directory, execute
```bash
python3 __main__.py
```

### Run from Executable
For Linux-systems, an executable is bundled for simplicity of use. This file
is located in the `dist` folder, or can be downloaded from the latest version.

## Allow all Ports
By default, all ports below 1024 (with the exception of port 0) require root
access. Execute the application as such to be able to capture all those
messages.

Capturing on port 0 is disallowed, since it commonly indicates "_choose any
valid port_".
