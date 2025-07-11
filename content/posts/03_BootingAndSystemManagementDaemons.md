---
Title: Booting and System Management Daemons (systemd)
Date: 2020-04-25
Author: smirza
Tags: linux, sysadmin, interview-notes, beginner
Keywords: linux, booting
Summary: Covers the boot process of a Linux/Unix machine in detail along with system management daemon - systemd. Also compares Legacy or traditional approach with what is being used now, when it comes to bootstrapping a machine and system management daemon.
Slug: booting-and-system-management-daemons-systemd
Status: published
---

## Boot process overview

Most Linux distributions now use a system manager daemon called **systemd** instead of the traditional UNIX **init.**

**systemd** streamlines the boot process by adding dependency management, support for concurrent startup processes, and a comprehensive approach to logging, among other features.

**System Booting:**

During bootstrapping, the kernel is loaded into memory and begins to execute. A variety of initialization tasks are performed, and the system is then made available to users. The general overview of this process is shown below:

![/static/img/posts/03_BootingAndSystemManagementDaemons/Linux_Boot_Final.png](/static/img/posts/03_BootingAndSystemManagementDaemons/Linux_Boot_Final.png)

_Admins can modify bootstrap configurations by editing config files for the system startup scripts or by changing the arguments the boot loader passes to the kernel._

_Before the system is fully booted, filesystems must be checked and mounted and system daemons started. These procedures are managed by a series of shell scripts (sometimes called “**init** scripts”) or unit files that are run in sequence by **init** or parsed by **systemd**._

## System Firmware

When a machine is powered on,

- the CPU is hardwired to execute boot code stored in ROM. (On Virtual systems, this "ROM" may be imaginary, but the concept remains the same.)
- System Firmware knows about all the devices that live on the motherboards, (such as SATA controllers, network interfaces, USB controllers, and sensors for power and temperature. (Virtual systems pretend to have this same set of devices.))
- System firmware allows hardware configuration of these devices and also lets you either expose or disable (hide) them to the operating system.

  Side Note: _On physical hardware (as opposed to virtual machines) the firmware offers a user interface. - press a particular key (magic key) immediately after powering on the system to access this._

- During normal bootstrapping, the system firmware probes for the h/w and disks, runs a simple set of health checks, and then looks for the next stage of bootstrapping code.
- The firmware UI lets you designating a boot device, (usually can be prioritised) DVD, USB, Hard disk.

  _In most cases if you are choosing a Disk drive it populates a secondary priority list. To boot from a particular drive, one must both set it as the highest priority disk and make sure that "hard disk" is enabled as a boot medium._

### BIOS vs. UEFI

BIOS (Basic Input/Output System)- Traditional / Legacy

**UEFI -** the Unified Extensible Firmware Interface

- BIOS has been supplanted by a more formalised and modern standard
- Often referred to as “UEFI BIOS”
- Most systems that implement UEFI can fall back to a legacy BIOS implementation if the operating system they’re booting doesn’t support UEFI.

  _UEFI is the current revision of an earlier standard, EFI._

  _Virtualised environments often adopt BIOS as their underlying boot mechanism, so the BIOS world isn’t in danger of extinction just yet. UEFI also builds-in several accommodations to the old BIOS regime, so a working knowledge of BIOS can be quite helpful for deciphering the UEFI documentation._

**Legacy BIOS**

_Partitioning is a way to subdivide physical disks. See this page for a more detailed discussion._

- BIOS assumes that the boot device starts with a record called the MBR (Master Boot Record).
- The **MBR** includes both a **first-stage boot loader** (aka “boot block”) and a **primitive disk partitioning table.**

  _The amount of space available for the boot loader is so small (less than 512 bytes) that it’s not able to do much other than load and run a second-stage boot loader._

- The boot block nor the BIOS is sophisticated enough to read any type of a standard Filesystem, so the second-stage boot loader must be kept somewhere easy to find.
- In one typical scenario, the boot block reads the partitioning information from the MBR and identifies the disk partition marked as “active.” It then reads and executes the second-stage boot loader from the beginning of that partition. This scheme is known as a **volume boot record.**
- Alternatively, the second-stage boot loader can live in the dead zone that lies between the MBR and the beginning of the first disk partition.
- For historical reasons, the first partition doesn’t start until the 64th disk block, so this zone normally contains at least 32KB of storage: still not a lot, but enough to store a filesystem driver.
- This storage scheme is commonly used by the GRUB boot loader; GRUB: the Grand Unified Boot loader.
- The MBR boot block is OS-agnostic. The second stage however is run from a particular location, there may be multiple versions that can be installed. The second-stage loader is generally knowledgeable about operating systems and filesystems, and usually has config options of its own.

**UEFI**

- UEFI specification includes a modern disk partitioning scheme known as **GPT** (GUID Partition Table, where GUID stands for “globally unique identifier”).
- UEFI also understands **FAT** (File Allocation Table) filesystems.
- These features combine to define the concept of an **EFI System Partition (ESP)**
- At boot time, the firmware consults the GPT to identify the ESP.
- It then reads the configured target application directly from a file in the ESP and executes it.
- Because the ESP is just a generic FAT filesystem, it can be mounted, read, written, and maintained by any operating system.
- No boot blocks are required anywhere on the disk.

  _Truth be told, UEFI does maintain an MBR-compatible record at the beginning of each disk to facilitate interoperability with BIOS systems. BIOS systems can’t see the full GPT-style partition table, but they at least recognise the disk as having been formatted._

- In the UEFI system, no boot loader at all is technically required.
- Boot target can be a UNIX or Linux kernel that has been configured for direct UEFI loading, thus effecting a loader-less bootstrap.

  _In practice, though, most systems still use a boot loader, partly because that makes it easier to maintain compatibility with legacy BIOSes._

- UEFI saves the pathname to load from the ESP as a configuration parameter.
- If UEFI finds no configuration it looks at default path, usually `/efi/boot/bootx64.efi` on modern Intel systems.
- A more typical path on a configured system (this one for Ubuntu and the GRUB boot loader) would be `/efi/ubuntu/grubx64.efi`.

  _Other distributions follow a similar convention._

- UEFI defines standard APIs for accessing the system’s hardware.
- Because UEFI has a formal API, you can examine and modify UEFI variables (including boot menu entries) on a running system.
- For example, `efibootmgr -v` shows the following summary of the boot configuration:

![/static/img/posts/03_BootingAndSystemManagementDaemons/27.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/27.jpg)

- efibootmgr lets you change the boot order, select the next configured boot option, or even create and destroy boot entries.

  _The ability to modify the UEFI configuration from user space means that the firmware’s configuration information is mounted read/write—a blessing and a curse. On systems (typically, those with systemd) that allow write access by default, rm -rf / can be enough to permanently destroy the system at the firmware level; in addition to removing files, rm also removes variables and other UEFI information accessible through /sys. Yikes! Don’t try this at home! (See [goo.gl/QMSiSG](http://goo.gl/QMSiSG), a link to a Phoronix article, for some additional details.)_

## Boot loaders

- The boot loader’s main job is to identify and load an appropriate operating system kernel. Most boot loaders can also present a boot-time user interface that lets you select which of several possible kernels or operating systems to invoke.
- Marshals the configuration arguments for the kernel.
- For Example - The argument single or -s usually tells the kernel to enter single-user mode instead of completing the normal boot process.
- Such options can be hard-wired into the boot loader’s configuration for every boot or can also be provided on the fly.

## GRUB

- The GRUB lineage has two main branches: the original GRUB, now called
  - GRUB Legacy
  - GRUB 2
- GRUB 2 has been the default boot manager for Ubuntu since version 9.10 and from RHEL 7

In this post we discuss only GRUB 2.

### GRUB Configuration

- Lets you specify parameters such as the kernel to boot and the operating mode to boot into.
- GRUB understands filesystem and reads the GRUB config from a text file stored in the root file system.
- The config file is called grub.cfg, and it’s usually kept in /boot/grub (/boot/grub2 in Red Hat and CentOS) along with a selection of other resources and code module that GRUB might need at boot time.
- Lets you change boot configurations by updating the grub.cfg file.
- Utilities like **grub-mkconfig** (RedHat and CentOS) and **update-grub** (Debian and Ubuntu).

_Most distributions assume that grub.cfg can be regenerated at will, and they do so automatically after updates. If you don’t take steps to prevent this, your handcrafted grub.cfg file will get clobbered._

- One can configure the GRUB using grub-mkconfig in a variety of ways. Most commonly the config is specified in `/etc/default/grub` in the form of sh variable assignments.

![/static/img/posts/03_BootingAndSystemManagementDaemons/29.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/29.jpg)

- After editing `/etc/default/grub`, run `update-grub` or `grub2-mkconfig` to translate your configuration into a proper grub.cfg file.
- You may edit `/etc/grub.d/40_custom` file to change the order in which kernels are listed in the boot menu, set a boot password, or change the names of boot menu items. As usual, run `update-grub` or `grub2-mkconfig` after making changes.

![/static/img/posts/03_BootingAndSystemManagementDaemons/30.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/30.jpg)

- Kernel paths are relative to the boot partition, which historically was mounted as /boot but with the advent of UEFI now is likely an unmounted EFI System Partition. Use `gpart show` and `mount` to examine your disk and determine the state of the boot partition.

**The GRUB command line**

GRUB supports a command-line interface for editing config file entries on the fly at boot time.

To enter command-line mode, type c at the GRUB boot screen.

From the command line, you can boot operating systems that aren’t listed in the grub.cfg file, display system information, and perform rudimentary filesystem testing.

Anything that can be done through grub.cfg can also be done through the command line.

![/static/img/posts/03_BootingAndSystemManagementDaemons/31.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/31.jpg)

### **Linux kernel options**

- Kernel startup options typically modify the values of kernel parameters
- Instruct the kernel to probe for particular devices
- Specify the path to the init or systemd process
- Designate a particular root device

![/static/img/posts/03_BootingAndSystemManagementDaemons/32.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/32.jpg)

- When specified at boot time, kernel options are not persistent. Edit the appropriate kernel line in /etc/grub.d/40_custom or /etc/defaults/grub to make the change permanent across reboots.

_Security patches, bug fixes, and features are all regularly added to the Linux kernel. Unlike other software packages, however, new kernel releases typically do not replace old ones. Instead, the new kernels are installed side by side with the previous versions so that you can return to an older kernel in the event of problems._

_This convention helps administrators back out of an upgrade if a kernel patch breaks their system, although it also means that the boot menu tends to get cluttered with old versions of the kernel. Try choosing a different kernel if your system won’t boot after an update._

## System Management Daemons

- Once the kernel has been loaded and has completed its initialization process, it creates a complement of “spontaneous” processes in user space. They’re called spontaneous processes because the kernel starts them autonomously.

  _Most of the spontaneous processes are really part of the kernel implementation. They don’t necessarily correspond to programs in the filesystem. They’re not configurable, and they don’t require administrative attention. You can recognize them in ps listings (see this page) by their low PIDs and by the brackets around their names (for example, [pagedaemon] on FreeBSD or [kdump] on Linux)._

- System management daemon (init): It has process ID 1 and usually runs under the name init. The system gives init a couple of special privileges, but for the most part it’s just a user-level program like any other daemon.

**Responsibilities of init**

Main goal is to make sure the system runs the right complement of services and daemons at any given time

To serve this goal, init maintains a notion of the mode in which the system should be operating. Some commonly defined modes:

- Single-user mode, in which only a minimal set of filesystems is mounted, no services are running, and a root shell is started on the console
- Multiuser mode, in which all customary filesystems are mounted and all configured network services have been started, along with a window system and graphical login manager for the console
- Server mode, similar to multiuser mode, but with no GUI running on the console.

Init normally takes care of many different startup chores as a side effect of its transition from bootstrapping to multiuser mode. These may include:

- Setting the name of the computer
- Setting the time zone
- Checking disks with fsck
- Mounting Filesystems
- Removing old files from the /tmp directory
- Configuring network interfaces
- Configuring packet filters
- Starting up other daemons and network services

init has very little built-in knowledge about these tasks. In simply runs a set of commands or scripts that have been designated for execution in that particular context.

**Implementations of init**

Three very different flavors of system management processes are in widespread use:

- An init styled after the init from AT&T’s System V UNIX, which we refer to as “traditional init.” This was the predominant init used on Linux systems until the debut of systemd.
- An init variant that derives from BSD UNIX and is used on most BSD-based systems, including FreeBSD, OpenBSD, and NetBSD. This one is just as tried-and-true as the SysV init and has just as much claim to being called “traditional,” but for clarity we refer to it as “BSD init.” This variant is quite simple in comparison with SysV-style init. We discuss it separately starting on this page.
- A more recent contender called systemd which aims to be one-stop-shopping for all daemon- and state-related issues. As a consequence, systemd carves out a significantly larger territory than any historical version of init. That makes it somewhat controversial, as we discuss below. Nevertheless, all our example Linux distributions have now adopted systemd.

_Although these implementations are the predominant ones today, they’re far from being the only choices. Apple’s macOS, for example, uses a system called launchd. Until it adopted systemd, Ubuntu used another modern init variant called Upstart._

_On Linux systems, you can theoretically replace your system’s default init with whichever variant you prefer. But in practice, init is so fundamental to the operation of the system that a lot of add-on software is likely to break. If you can’t abide systemd, standardize on a distribution that doesn’t use it_.

### **Traditional Init**

**Run levels:**

In the traditional init world, system modes (e.g., single-user or multiuser) are known as “run levels.” Most run levels are denoted by a single letter or digit. Most run levels are denoted by a single letter or digit.

Traditional init does have a number of notable shortcomings:

- The traditional init on its own is not really powerful enough to handle the needs of a modern system.
- Most systems that use it actually have a standard and fixed init configuration that never changes.
- That configuration points to a second tier of shell scripts that do the actual work of changing run levels and letting administrators make configuration changes.
- The second layer of scripts maintains yet a third layer of daemon- and system-specific scripts, which are cross-linked to run-level-specific directories that indicate what services are supposed to be running at what run level. (Not the best design!)
- This system has no general model of dependencies among services, so it requires that all startups and takedowns be run in a numeric order that’s maintained by the administrator.
- Later actions can’t run until everything ahead of them has finished, so it’s impossible to execute actions in parallel, and the system takes a long time to change states.

### systemd vs. the world

systemd takes all the init features formerly implemented with sticky tape, shell script hacks, and the sweat of administrators and formalises them into a unified field theory of how services should be configured, accessed, and managed.

- Like package management, systemd defines a robust dependency model, not only among services but also among “targets,” systemd’s term for the operational modes that traditional init calls run levels.
- systemd not only manages processes in parallel, but also manages network connections (**networkd**), kernel log entries (**journald**), and logins (**logind**).

## SYSTEMD in Detail

systemd is not a single daemon but **a collection of programs, daemons, libraries, technologies, and kernel components.**

_A full build of the project generates 69 different binaries. Think of it as a scrumptious buffet at which you are forced to consume everything._

_Since systemd depends heavily on features of the Linux kernel, it’s a Linux-only proposition. You won’t see it ported to BSD or to any other variant of UNIX within the next five years._

**Units and unit files**

- An entity that is managed by systemd is known generically as a unit.
- A unit can be “a service, a socket, a device, a mount point, an auto-mount point, a swap file or partition, a startup target, a watched filesystem path, a timer controlled and supervised by systemd, a resource management slice, a group of externally created processes.
- Within systemd, the behavior of each unit is defined and configured by a unit file.
- In the case of a service, for example, the unit file specifies the location of the executable file for the daemon, tells systemd how to start and stop the service, and identifies any other units that the service depends on. (unit files are written in ini formats)
- A sample unit file (eg. rsync.service)

![/static/img/posts/03_BootingAndSystemManagementDaemons/36.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/36.jpg)

---

Side Note:

[Install] section is mandatory here, because it tells systemd at which moment during boot process your service should be started. You process should be linked to some generic boot targets such as multi-user.target or graphical.target, or to a special purpose target (such as network-online.target), or a custom local target.

Example:

```
[Install]
WantedBy=multi-user.target
```

Here systemd will inject your service as a dependency for multi-user.target. systemd will start your service whenever multi-user target is started.

systemd reads files (or symlinks) in its configuration directories to see which units should be started in what order. systemctl enable creates such symlinks for services that it already knows, and places these symlinks at the points at the boot process when the service should be started (e.g. in special multi-user.target.wants/ subdirectory.)

There is also another way how operating system uses `systemd` to start its own services at startup. It is not something that should you do, but since the question is about `[Install]` section...

There are `systemd` units called "**static**" units and they are not managed by `systemctl enable` (or `systemctl disable`.) They are started on boot through hardcoded symlinks in `/usr/lib/systemd/system/` (instead of `/etc/systemd/system/`), and if you encounter them while looking at units in your system... know that they don't have `[Install]` section.

---

- Unit files can live in several different places. /usr/lib/systemd/system is the main place where packages deposit their unit files during installation; on some systems, the path is /lib/systemd/system instead.
- The contents of this directory are considered stock, so you shouldn’t modify them.
- Your local unit files and customisations can go in /etc/systemd/system.
- There’s also a unit directory in /run/systemd/system that’s a scratch area for transient units.

  _There is also a location for run-time unit definitions at `/run/systemd/system`. Unit files found in this directory have a priority landing between those in `/etc/systemd/system` and `/lib/systemd/system`. Files in this location are given less weight than the former location, but more weight than the latter._

  _The `systemd` process itself uses this location for dynamically created unit files created at runtime. This directory can be used to change the system’s unit behaviour for the duration of the session. All changes made in this directory will be lost when the server is rebooted._

- systemd maintains a telescopic view of all these directories, so they’re pretty much equivalent.
- If there’s any conflict, the files in /etc have the highest priority.
- By convention, unit files are named with a suffix that varies according to the type of unit being configured. For example, service units have a .service suffix and timers use .timer.
- Within the unit file, some sections (e.g., [Unit]) apply generically to all kinds of units, but others (e.g., [Service]) can appear only in the context of a particular unit type.

**systemctl: manage systemd**

- systemctl is an all-purpose command for investigating the status of systemd and making changes to its configuration.
- Running systemctl without any arguments invokes the default list-units subcommand, which shows all loaded and active services, sockets, targets, mounts, and devices. To show only loaded and active services, use the `--type=service` qualifier:

![/static/img/posts/03_BootingAndSystemManagementDaemons/37.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/37.jpg)

- It’s also sometimes helpful to see all the installed unit files, regardless of whether or not they’re active:

![/static/img/posts/03_BootingAndSystemManagementDaemons/38.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/38.jpg)

- For subcommands that act on a particular unit (e.g., systemctl status) systemctl can usually accept a unit name without a unit-type suffix (e.g., cups instead of cups.service). However, the default unit type with which simple names are fleshed out varies by subcommand.

![/static/img/posts/03_BootingAndSystemManagementDaemons/39.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/39.jpg)

**Unit statuses**

In the output of systemctl list-unit-files above, we can see that cups.service is disabled. We can use systemctl status to find out more details:

![/static/img/posts/03_BootingAndSystemManagementDaemons/40.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/40.jpg)

- Here, systemctl shows us that the service is currently inactive (dead) and tells us when the process died.
- Also shows the service defaults to being enabled at startup, but that it is presently disabled.
- The last four lines are recent log entries. By default, the log entries are condensed so that each entry takes only one line. This compression often makes entries unreadable, so we included the -l option to request full entries. It makes no difference in this case, but it’s a useful habit to acquire.

![/static/img/posts/03_BootingAndSystemManagementDaemons/41.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/41.jpg)

- The enabled and disabled states apply only to unit files that live in one of systemd’s system directories (that is, they are not linked in by a symbolic link) and that have an [Install] section in their unit files.
- “Enabled” units should perhaps really be thought of as “installed,” meaning that the directives in the [Install] section have been executed and that the unit is wired up to its normal activation triggers. In most cases, this state causes the unit to be activated automatically once the system is bootstrapped.
- "Disabled" - Which means the service is present but not started autonomously. You can manually activate a unit that is disabled by running `systemctl start`; `systemd` wont complain.
- Many units have no installation procedure, so they can’t truly be said to be enabled or disabled; they’re just available. Such units’ status is listed as **static**. These only become active if activated by hand (`systemctl start`) or named as a dependency of other active units.
- Unit files that are **linked** were created with `systemctl link`. This command creates a symbolic link from one of systemd’s system directories to a unit file that lives elsewhere in the filesystem. Such unit files can be addressed by commands or named as dependencies, but they are not full citizens of the ecosystem and have some notable quirks. For example, running `systemctl disable` on a linked unit file deletes the link and all references to it. (this is not the best approach, instead just make copies.)
- The **masked** status means “administratively blocked.” `systemd` knows about the unit, but has been forbidden from activating it or acting on any of its configuration directives by `systemctl mask`. As a rule of thumb, turn off units whose status is enabled or linked with `systemctl disable` and reserve `systemctl mask` for static units.

We can use the following commands to enable a service and start it.

![/static/img/posts/03_BootingAndSystemManagementDaemons/42.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/42.jpg)

**Targets**

- Unit files can declare their relationships to other units in a variety of ways.

![/static/img/posts/03_BootingAndSystemManagementDaemons/36%201.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/36%201.jpg)

- The WantedBy clause says that if the system has a multi-user.target unit, that unit should depend on this one (rsync.service) when this unit is enabled.
- Since units directly support dependency management, no additional machinery is needed to implement the equivalent of init's run levels.
- systemd does define a distinct class of units (of type .**target**) to act as well known markers for common operating modes.
- Targets have no real superpowers beyond the dependency management that is available to any other unit.

_Traditional init defines at least seven numeric run levels, but many of those aren’t actually in common use. In a perhaps-ill-advised gesture toward historical continuity, systemd defines targets that are intended as direct analogs of the `init` run levels (`runlevel0.target`, etc.). It also defines mnemonic targets for day-to-day use such as `poweroff.target` and `graphical.target`. Table shows the mapping between init run levels and systemd targets._

![/static/img/posts/03_BootingAndSystemManagementDaemons/43.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/43.jpg)

- The only targets to really be aware of are `multi-user.target` and `graphical.target` for day-to-day use, and `rescue.target` for accessing single-user mode.
- To change the system’s current operating mode, use the `systemctl isolate` command:

  ```bash
  sudo systemctl isolate multi-user.target
  ```

- The `isolate` subcommand activates the stated target and its dependencies but deactivates all other units.

  _Under traditional init, you use the `telinit` command to change run levels once the system is booted. Some distributions now define `telinit` as a symlink to the `systemctl` command, which recognizes how it’s being invoked and behaves appropriately._

- To see the target the system boots into by default, run the `get-default subcommand:

  ```bash
  $ systemctl get-default
  graphical.target
  ```

- To change the default target

  ```bash
  $ sudo systemctl set-default multi-user.target
  ```

- To see all the system's available target, run `systemctl list-units`:

  ```bash
  $ systemctl list-units --type=target
  ```

**Dependancies among units**

- Not all dependencies are explicit.
- systemd takes over the functions of the old inetd and also extends this idea into the domain of the D-Bus interprocess communication system.

  _inetd (Side Note) : The inetd daemon is a superserver that standardizes network port access and interfaces between regular programs and network ports. After you start inetd, it reads the inetd.conf file and then listens on the network ports defined in that file, attaching a newly started process to every new incoming connection._

- systemd knows which network ports or IPC connection points a given service will be hosting, and it can listen for requests on those channels without actually starting the service.
- If a client does materialise, systemd simply starts the actual service and passes off the connection. The service runs if it’s actually used and remains dormant otherwise.
- systemd makes some assumptions about the normal behavior of most kinds of units. The exact assumptions vary by unit type.
- For example, systemd assumes that the average service is an add-on that shouldn’t be running during the early phases of system initialisation. Individual units can turn off these assumptions with the line, in the [Unit] section of their unit file; the default is true.

  ```bash
  DefaultDependencies=false
  ```

- A third class of dependencies are those explicitly declared in the [Unit] sections of unit files.

  - Explicit dependencies in the [Unit] section of unit files

![/static/img/posts/03_BootingAndSystemManagementDaemons/49.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/49.jpg)

- With the exception of Conflicts, all the options express the basic idea that the unit being configured depends on some set of other units.
- The least restrictive variant, Wants, is preferred when possible.
- You can extend a unit’s Wants or Requires cohorts by creating a unit-file.wants or unit-file.requires directory in /etc/systemd/system and adding symlinks there to other unit files.
- You can let systemctl do it for you. For example, the command adds a dependency on my.local.service to the standard multiuser target, ensuring that the service will be started whenever the system enters multiuser mode.

  ```bash
  $ sudo systemctl add-wants multi-user.target my.local.service
  ```

- The [Install] clauses themselves have no effect in normal operation, so if a unit doesn’t seem to be started when it should be, make sure that it has been properly enabled and symlinked.

**Execution Order**

- In systemd, the order in which units are activated (or deactivated) is an entirely separate question from that of which units to activate.
- When the system transitions to a new state, systemd first traces the various sources of dependency information outlined in the previous section to identify the units that will be affected.
- It then uses Before and After clauses from the unit files to sort the work list appropriately. To the extent that units have no Before or After constraints, they are free to be adjusted in parallel.
- systemd facilitates parallelism.
- Units do not acquire serialisation dependencies unless they explicitly ask for them.

**A more complex unit file example**

A unit file for the NGINX web server, **_nginx.service:_**

![/static/img/posts/03_BootingAndSystemManagementDaemons/51.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/51.jpg)

- Service is of type `forking`, which means that the start up command is expected to **terminate** even though the actual daemon continues running in the background.
- systemd won’t have directly started the daemon, the daemon records its PID (process ID) in the stated `PIDFile` so that systemd can determine which process is the daemon’s primary instance.
- The `Exec` lines are commands to be run in various circumstances. `ExecStartPre` commands are run before the actual service is started; the ones shown here validate the syntax of NGINX’s configuration file and ensure that any preexisting PID file is removed.
- `ExecStart` is the command that actually starts the service.
- `ExecReload` tells systemd how to make the service reread its configuration file.

  systemd automatically sets the environment variable MAINPID to the appropriate value.)

- Termination for this service is handled through `KillMode` and `KillSignal`, which tell systemd that the service daemon interprets a QUIT signal as an instruction to clean up and exit. The line would have essentially the same effect. If the daemon doesn’t terminate within `TimeoutStopSec` seconds, systemd will force the issue by pelting it with a TERM signal and then an uncatchable KILL signal.

  ```bash
  ExecStop=/bin/kill -s HUP $MAINPID
  ```

- The `PrivateTmp` setting is an attempt at increasing security.
- It puts the service’s `/tmp` directory somewhere other than the actual `/tmp`, which is shared by all the system’s processes and users.

**Local services and customisations**

- It’s relatively trivial to create a unit file for a home-grown service.
- Browse the examples in `/usr/lib/systemd/system` and adapt one that’s close to what you want. See man page of systemd for reference.
- Put your new unit file in `/etc/systemd/system`. You can then run to activate the dependencies listed in the service files's install section.

```bash
$ sudo systemctl enable custom.service
```

- For customisation, you should never edit a unit file you did not write.

  _Instead, create a configuration directory in `/etc/systemd/system/unit-file.d` and add one or more configuration files there called `xxx.conf`. The xxx part doesn’t matter; just make sure the file has a `.conf` suffix and is in the right location. `override.conf` is the standard name. Override files have priority over the original unit file should both sources try to set the value of a particular option._

_Looking at an example:_

Suppose that a sites NGINX configuration file in a nostandard place, say, `/usr/local/www/nginx.conf`. You need to run nignx with `-c /usr/local/www/nginx.conf` option so that it can . find the proper configuration file.

You can’t just add this option to `/usr/lib/systemd/system/nginx.service` because that file will be replaced whenever the NGINX package is updated or refreshed. Instead, you can use the following command sequence:

![/static/img/posts/03_BootingAndSystemManagementDaemons/54.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/54.jpg)

- The first ExecStart= removes the current entry
- The second sets an alternative start command. systemctl daemon-reload makes systemd re-parse unit files.
- However, it does not restart daemons automatically, so you’ll also need an explicit systemctl restart to make the change take effect immediately.
- This command sequence is such a common idiom that systemctl now implements it directly:

![/static/img/posts/03_BootingAndSystemManagementDaemons/55.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/55.jpg)

- You must still do the restart by hand
- override files is that they can’t modify the `[Install]` section of a unit file. Any changes you make are silently ignored. Just add dependencies directly with `systemctl add-wants` or `systemctl add-requires`.

Some Red Hat and CentOS boot chores continue to use config files found in the `/etc/sysconfig` directory and does not take into consideration systemd however they might be linked.

![/static/img/posts/03_BootingAndSystemManagementDaemons/57.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/57.jpg)

Files and subdirectories of Red Hat’s /etc/sysconfig directory

![/static/img/posts/03_BootingAndSystemManagementDaemons/58.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/58.jpg)

**systemd logging**

- systemd uses a universal framework that includes all kernel and service messages from early boot to final shutdown with journald daemon.
- System messages captured by `journald` are stored in the `/run` directory.
- `rsyslog` can process these messages and store them in traditional log files or forward them to a remote syslog server.
- You can also access the logs directly with the `journalctl` command. With no arguments it displays all log entries (oldest first).
- You can configure journald to retain messages from prior boots.
- To do this, edit `/etc/systemd/journald.conf` and configure the Storage attribute:

![/static/img/posts/03_BootingAndSystemManagementDaemons/60.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/60.jpg)

- Once you’ve configured `journald`, you can obtain a list of prior boots with

![/static/img/posts/03_BootingAndSystemManagementDaemons/61.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/61.jpg)

- You can then access messages from a prior boot by referring to its index or by naming its long-form ID

![/static/img/posts/03_BootingAndSystemManagementDaemons/62.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/62.jpg)

- To restrict the logs to those associated with a specific unit, use the -u flag:

![/static/img/posts/03_BootingAndSystemManagementDaemons/63.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/63.jpg)

## Reboot and shutdown procedures

**Shutting down physical systems**

- The **halt** command performs the essential duties required for shutting down the system.
- **halt** logs the shutdown, kills nonessential processes, flushes cached filesystem blocks to disk, and then halts the kernel.
- On most systems, **halt -p** powers down the system as a final flourish.
- **reboot** is essentially identical to **halt**, but it causes the machine to **reboot** instead of halting.
- The **shutdown** command is a layer over halt and reboot that provides for scheduled shutdowns and ominous warnings to logged-in users.
- **shutdown** does nothing of technical value beyond halt or reboot, so feel free to ignore it if you don’t have multiuser systems.

## Stratagems for a non-booting system

Three basic approaches to this situation, listed here in rough order of desirability:

- Don’t debug; just restore the system to a known-good state.
- Bring the system up just enough to run a shell, and debug interactively.
- Boot a separate system image, mount the sick system’s filesystems, and investigate from there.

The “boot to a shell” mode is known generically as single-user mode or rescue mode. Systems that use systemd have an even more primitive option available in the form of emergency mode; it’s conceptually similar to single-user mode, but does an absolute minimum of preparation before starting a shell.

_Because single-user, rescue, and emergency modes don’t configure the network or start network-related services, you’ll generally need physical access to the console to make use of them. As a result, single-user mode normally isn’t available for cloud-hosted systems._

**Single User Mode**

- Also known as `rescue.target` on systems that use systemd.
- Only a minimal set of processes, daemons, and services are started.
- The root filesystem is mounted (as is /usr, in most cases), but the network remains uninitialized.
- At boot time, you request single-user mode by passing an argument to the kernel, usually single or -s
- You can do this through the boot loader’s command-line interface. In some cases, it may be set up for you automatically as a boot menu option.

  _If the system is already running, you can bring it down to single-user mode with a shutdown (FreeBSD), telinit (traditional init), or systemctl (systemd) command._

  _Sane systems prompt for the root password before starting the single-user root shell. Unfortunately, this means that it’s virtually impossible to reset a forgotten root password through single-user mode. If you need to reset the password, you’ll have to access the disk by way of separate boot media._

- You can execute commands in much the same way as when logged in on a fully booted system.
- However, sometimes only the root partition is mounted; you must mount other filesystems manually to use programs that don’t live in /bin, /sbin, or /etc.
- You can often find pointers to the available filesystems by looking in /etc/fstab.
- Under Linux, you can run fdisk -l (lowercase L option) to see a list of the local system’s disk partitions.
- In single-user environments, the filesystem root directory starts off being mounted read-only.
- If /etc is part of the root filesystem (the usual case), it will be impossible to edit many important configuration files. To fix this problem, you’ll have to begin your single-user session by remounting / in read/write mode.

  ```bash
  mount -o rw,remount /
  ```

  _Single-user mode in Red Hat and CentOS is a bit more aggressive than normal. By the time you reach the shell prompt, these systems have tried to mount all local filesystems. Although this default is usually helpful, it can be problematic if you have a sick filesystem. In that case, you can boot to emergency mode by adding `systemd.unit=emergency.target` to the kernel arguments from within the boot loader (usually GRUB). In this mode, no local filesystems are mounted and only a few essential services are started._

  _The fsck command is run during a normal boot to check and repair filesystems. Depending on what filesystem you’re using for the root, you may need to run fsck manually when you bring the system up in single-user or emergency mode._

**Single-user mode with GRUB**

- On systems that use `systemd`, you can boot into rescue mode by appending `systemd.unit=rescue.target` to the end of the existing Linux kernel line.
- At the GRUB splash screen, highlight your desired kernel and press the “e” key to edit its boot options.
- Similarly, for emergency mode, use systemd.unit=emergency.target.

Example:

![/static/img/posts/03_BootingAndSystemManagementDaemons/70.jpg](/static/img/posts/03_BootingAndSystemManagementDaemons/70.jpg)

**Recovery of cloud systems**

- Backups are important for all systems, but cloud servers are particularly easy to snapshot.
- Providers charge extra for backups, but they’re inexpensive.
- Be liberal with your snapshots and you’ll always have a reasonable system image to fall back on at short notice.

  _From a philosophical perspective, you’re probably doing something wrong if your cloud servers require boot-time debugging. Pets and physical servers receive veterinary care when they’re sick, but cattle get euthanized. Your cloud servers are cattle; replace them with known-good copies when they misbehave. Embracing this approach helps you not only avoid critical failures but also facilitates scaling and system migration._

  Within AWS, single-user and emergency modes are unavailable. However, EC2 filesystems can be attached to other virtual servers if they’re backed by Elastic Block Storage (EBS) devices. This is the default for most EC2 instances, so it’s likely that you can use this method if you need to. Conceptually, it’s similar to booting from a USB drive so that you can poke around on a physical system’s boot disk.

  Here’s what to do:

  - Launch a new instance in the same availability zone as the instance you’re having issues with. Ideally, this recovery instance should be launched from the same base image and should use the same instance type as the sick system.

  - Stop the problem instance. (But be careful not to “terminate” it; that operation deletes the boot disk image.)

  - With the AWS web console or CLI, detach the volume from the problem system and attach the volume to the recovery instance.

  - Log in to the recovery system. Create a mount point and mount the volume, then do whatever’s necessary to fix the issue. Then unmount the volume. (Won’t unmount? Make sure you’re not cd’ed there.)

  - In the AWS console, detach the volume from the recovery instance and reattach it to the problem instance. Start the problem instance and hope for the best.

### Additional Resources

- [Understanding Systemd Units and Unit Files](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)

  ***
