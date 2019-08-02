# Install prerequisites

Installing the prerequisites differs on the different operating systems and is therefore covered in different sections. Here, you need to use the superuser.

## Linux

We recommend to install the prerequisites using the packaging system of your distribution. On Debian/Ubuntu use:

```bash
sudo apt install build-essential python3-dev python3-pip python3-venv 
```

on RHEL/CentOS use:

```bash

```

On Ubuntu 14.04, `python3-venv` is not available. Please use `python3.5-venv` instead.

On RHEL/CentOS `selinux` is enabled by default. This can result in unexpected errors, depending on where you store the source code on the system. While the prefereble way is to configure it correctly (which is beyond the scope of this documentation), you can also set `selinux` to `permissive` or `disabled` in `/etc/selinux/config` (and reboot afterwards).

## macOS

We recommend to install the prerequisites using [brew](http://brew.sh):

```bash
brew install python3        # for python 3
brew install git
```

## Windows

On Windows, the software prerequisites need to be downloaded and installed from their particular web sites.

For python:
* download from <https://www.python.org/downloads/windows/>
* we recommend a version >= 3.6
* don't forget to check 'Add Python to environment variables' during setup

For git:
* download from <https://git-for-windows.github.io/>

For the Microsoft C++ Build Tools:
* download from <https://wiki.python.org/moin/WindowsCompilers>

All further steps need to be performed using the windows shell `cmd.exe`. You can open it from the Start-Menu.
