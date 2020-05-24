# PySysLogQt
Extremely simple `syslog` server written in `Python 3`, for those who do not
want to install a complex `syslog` server, or write their own.

## Features:
* Lightweight and graphical!
* Accepts messages according to the `RFC 5424` format, but also allows the
  simplified `Python`-format (`<PRI>MESSAGE\000`)!
* Save the messages to a file for later use!
* Load a file of previously saved messages!
* Sort all messages!
* Filter all messages with [complex filters](./Filter.md)!
* Color-coded records for all severity levels!
* Hide unwanted information!

## Requirements:
* `PyQt5`
* `lark-parser`
* `rfc5424-logging-handler`
* `dateutil`

## Execution
#### Command Line Arguments
`PySysLogQt` can be launched with command line arguments. Use the `-h` or
the `--help` flag to get the help menu:
```
usage: PySysLogQt [-h] [-H [HOST]] [-P [PORT]] [-c]

Starts a syslog server.

optional arguments:
  -h, --help            show this help message and exit
  -H [HOST], --host [HOST]
                        The host to listen on. Defaults to "localhost".
  -P [PORT], --port [PORT]
                        The port to listen on. Defaults to 1024.
  -c, --cli             When set, the command line interface is used over the
                        GUI.
```
#### Run from Source
Make sure you have `Python 3` and all requirements installed.
In the root directory, execute
```bash
python3 __main__.py -h
```

Note that this gives the `help`-menu.

#### Run from Executable
For Linux-systems, an executable is bundled for simplicity of use. This file
is located in the `dist` folder, or can be downloaded from the latest version.

#### Load a File on Launch
When setting the `HOST` to `file://<myfile>`, the server will not listen to
traffic, but instead open the file called `<myfile>`. The port will be
ignored in this case. Note that, the first two slashes are **not** part of
the filename.

## Issues
#### Allow all Ports
By default, all ports below 1024 (with the exception of port 0) require root
access. Execute the application as such to be able to capture all those
messages.

Capturing on port 0 is disallowed, since it commonly indicates "_choose any
valid port_".

#### Not seeing your messages?
It is perfectly possible that your messages are not being displayed. Make
sure:
* The `host` and `port` are set to the correct source.
* The logger is not muting the messages. Often, `WARNING` messages are set to
  be the lowest level of messages that are sent, implicitly muting all
  `DEBUG`, `INFO` and `NOTICE` messages.
