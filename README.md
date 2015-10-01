# PyNas
Application turning ubuntu server into a fully functional home file server.

## Long term projects aim
The projects aims to create a stand alone application capable of configuring and maintaining a stand-alone file server providing the following functionalities:
  - Everything should be properly secured by encryption and lack of bugs ;]
  - Accessing files over LAN
  - Accessing files over web GUI 
  - Synchronizing files over the Internet
  - Selecting shares that are supposed to keep old file versions
  - Selecting shares to be regularly backed up to a specified destination
  - Selecting which files are to be backed up using filters capable of differentiate by file name, type and size
  - Mixing three above techniques in any way
  - Backing up of the whole server or some parts of its data to other PyNas server that is in possession of a friend
  - PIM services
  - Email web client and backup
  - RSS/Atom reader web application

## Execution order
The mentioned functionality will be implemented in the following order:
  - Hard drives and partitions detection, verification and mounting according to a config file
  - Hard drives power management using hdparm
  - [not sure] Integration with NFS
  - Integration with SAMBA server
  - Integration of SAMBA with LDAP server as a user backedn
  - Integration with Owncloud - WebGui + PIM services + RSS/Atom reader
  - Integration wit local mirrowing email server + Ownclouds email client
  - Creation of own FUSE based file system capable of COW and file versioning
  - Implement functionality to synchronize the file system over the Internet
  - Replace Owncloud sync client with created mechanism
 
## License
PyNas is distributed unde The BSD 3-Clause License, so feel free to fork and cooperate.

## Side quests
This project is intended as a good excuse to properly learn the Python and finally create an ultimate home file + PIM + Backup solution that can used without relaying on any external company. Whole server has to be usable on not-so-high-end machines as older Notebooks and arm development platforms like Odroid C1.

## Jokes and tits
Rumor has it that those French tanks have 6 gears, 5 reverse and 1 forward.  Just in case they're attacked from behind, that's where the forward gear comes in handy.

Sorry, no tities this time, wait the next commit.
