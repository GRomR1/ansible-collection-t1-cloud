==========================
T1 Cloud Compute Instance
==========================

.. contents:: Topics


v1.0.0
======

Release Summary
---------------

Initial release of the T1 Cloud Compute Instance collection.

Major Changes
-------------

- Initial implementation of ``t1_cloud_vm`` module for managing T1 Cloud virtual machines
- Added ``t1_cloud_iam_token`` lookup plugin for authentication
- Support for full VM lifecycle management (create, start, stop, delete)
- Configuration of VM resources (CPU, RAM, disk storage)
- Network configuration including public IP assignment
- Support for additional disk volumes
- SSH key and cloud-init user data configuration
- Security groups and labels support

New Modules
-----------

- gromr10.compute_instance.t1_cloud_vm - Manage virtual machines in T1 Cloud

New Lookup Plugins
------------------

- gromr10.compute_instance.t1_cloud_iam_token - Obtain access token for T1 Cloud authentication

Breaking Changes
----------------

- N/A (Initial release)

Deprecated Features
-------------------

- N/A (Initial release)

Removed Features (previously deprecated)
----------------------------------------

- N/A (Initial release)

Security Fixes
--------------

- N/A (Initial release)

Bugfixes
--------

- N/A (Initial release)

Known Issues
------------

- N/A (Initial release)
