# So you want to install Arch Linux?

<time datetime="2013-12-13">December 13th, 2013</time>

Arch Linux is a great operating system. It's rolling release, so your software
is always up to date and secure. It has a great package manger, a great
community and it comes installed with the bare minimum – a plus when you want to
configure your system exactly the way you want, without having anything extra on
top.

Arch Linux isn't for everyone, there are quite a few things you should consider
before jumping in. You will need to have a basic understanding of Linux command
line as Arch Linux does not do a lot of hand holding. If you aren't familiar
with using commands in a console, definitely read up and learn a bit before
continuing.

## Prerequesites

Installing and running Arch Linux requires a regular connection to the internet
and regular maintenance. You will need to pay attention to updates, read change
logs, and merge new configuration files. (really you should do this with all
Linux distributions, but Arch is particularly unforgiving of lazy admins.) If
you don't have this sort of time or don't have a regular internet connection,
Arch Linux may not be the right choice. Neglecting maintenance and not updating
properly can cause your system to crash and make running Arch Linux an
unenjoyable experience.

## Let's do this!

If you are still set on installing Arch Linux at this point, then its time to
get started.

I would highly recommend reading through the
[Beginners Guide](https://wiki.archlinux.org/index.php/Beginners%27_Guide)
completely before installing Arch Linux. You should also look up your hardware's
Linux compatibility, and if you need special drivers, have them on a thumb drive
so you can easily install them when you need to.

### Here is an overview of the installation process:

1. Make installation media
2. Boot install media
3. Establish a network connection - ussually works out of box with ethernet
4. Partition your harddrive if it isn't already partitioned
5. Format the partitions you are installing to
6. Mount the partitions
7. Choose mirrors for pacman in /etc/pacman.d/mirrorlist
8. Install the base system with pacstrap
9. Generate an /etc/fstab file

At this point Arch Linux is installed, but you will want to do some initial
configuration through chroot before booting in the new system. Specifically the
following:

1. Install and configure a bootloader
2. Install fonts
3. Set locale, keymap, timezone, system time, hostname and root password

At this point you can boot into your new install, setup audio, configure
graphics, and install a desktop environment/window manager of your choice. The
options are limitless and you can really make it your own.

## Keeping your system stable

As I mentioned before, if you aren't careful with updates and maintenance, there
is the possibility that your Arch Linux install will break. Arch Linux isn't
unstable, but you do need to administer it properly.

Our website and services are run off [Digital Ocean](https://www.digitalocean.com/)
droplets (virtual private servers) with Arch Linux. We have great uptime and
system stability. If you follow the following tips, you can achieve the same
results.

### Update every week and read the news

I personally do updates every Friday afternoon. Updating usually takes about 15
minutes at the most. First make sure to read the news at
https://www.archlinux.org/news/. Pay special attention to items labeled “manual
intervention required”. This means you need to take some sort of action to
prevent breakage and update properly.

After you check the news, run pacman -Syu and pay attention to what is being
updated as well as any messages printed to the screen. Follow up with any
instructions if there are any.

If any critical packages are updated, such as the kernel or X server, read the
change log for that package. It could give you information on exciting new
features or potential issues to watch out for. It may help to subscribe to the
news lists for software you want to keep an eye on.

The final step is to [merge .pac files](https://wiki.archlinux.org/index.php/Pacnew_and_Pacsave_Files#Managing_.pacnew_Files)
(this means .pacnew and .pacsave files) These files are created when packages
are updated and the configuration files for those packages have been changed.

Use find to get a list of .pac files in your system:

    find /etc -regextype posix-extended -regex ".+\.pac(new|save|orig)" 2> /dev/null

Then you need to compare the .pac file to the original configuration file, and
make changes appropriately. Don't just delete your old configuration files and
replace them with new ones, or delete all .pac files without looking at them.
This can potentially cause problems and instability.

Once you are done merging .pac files, your update is complete. If the Linux
kernel or any hardware drivers were updated, you may want to reboot.

### Don't install untrusted or beta software packages

You'd think this would be obvious, but it needs to be said. Installing beta
software, [AUR](https://aur.archlinux.org/) (arch user repository) packages,
software off git and compiling things from random websites can make your
computer buggy and unstable.

If you really want to try something out, sandbox it and don't install on your
main system.

You may be surprised at my mention of AUR packages, but keep in mind that these
packages can be uploaded by anyone. You have to be very prudent when using them
and realize that if an AUR package breaks your Arch Linux system, this isn't an
Arch Linux problem and is not officially supported. The AUR is a wonderful
resource, but it can also cause problems for new users and the less prudent.

## Install Days

Arch Women hosts Arch install days every few months. We answer questions and
chat with new users in our IRC channel ```#archlinux-women``` on
```irc.freenode.org``` Come install Arch Linux with us, ask questions, and have
a good time.
