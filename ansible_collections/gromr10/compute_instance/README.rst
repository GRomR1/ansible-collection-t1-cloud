T1 Cloud Compute Instance Collection
====================================

.. contents:: Topics


This collection provides Ansible modules and plugins for managing T1 Cloud compute instances and infrastructure.

Description
-----------

The ``gromr10.compute_instance`` collection includes modules and plugins for automating T1 Cloud virtual machine lifecycle management. It supports creating, configuring, starting, stopping, and deleting virtual machines in the T1 Cloud platform.

Supported ansible-core versions
--------------------------------

* ansible-core 2.9.10 or newer

Included content
----------------

.. Modules


Modules
~~~~~~~

.. autosummary::
   :toctree:

   t1_cloud_vm

.. Lookup plugins


Lookup plugins
~~~~~~~~~~~~~~

.. autosummary::
   :toctree:

   t1_cloud_iam_token

Installation and Usage
----------------------

Installing the Collection from Ansible Galaxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before using the collection, you need to install it with the Ansible Galaxy CLI:

.. code-block:: bash

    ansible-galaxy collection install gromr10.compute_instance

You can also include it in a ``requirements.yml`` file and install it with ``ansible-galaxy collection install -r requirements.yml``, using the format:

.. code-block:: yaml

    ---
    collections:
      - name: gromr10.compute_instance

Using modules from the collection in your playbooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can either call modules by their Fully Qualified Collection Namespace (FQCN), such as ``gromr10.compute_instance.t1_cloud_vm``, or you can call modules by their short name if you list the collection in the playbook's ``collections`` keyword:

.. code-block:: yaml

    ---
    - hosts: localhost
      collections:
        - gromr10.compute_instance
      tasks:
        - name: Create T1 Cloud VM
          t1_cloud_vm:
            api_token: "{{ t1_cloud_api_token }}"
            project_id: "{{ t1_cloud_project_id }}"
            name: "my-vm"
            image_id: "ubuntu-20.04"
            flavor_id: "small"
            subnet_id: "{{ subnet_id }}"
            state: present

Authentication
--------------

The collection supports authentication through API tokens. You can obtain an API token from the T1 Cloud console.

For security, it's recommended to use Ansible Vault to encrypt sensitive data like API tokens:

.. code-block:: yaml

    # In your playbook or vars file
    t1_cloud_api_token: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              66386439653...

You can also use the included lookup plugin to obtain IAM tokens:

.. code-block:: yaml

    - name: Get IAM token
      set_fact:
        api_token: "{{ lookup('gromr10.compute_instance.t1_cloud_iam_token',
                       auth_method='service_account',
                       client_id=service_account_id,
                       client_secret=service_account_secret) }}"

Examples
--------

Creating a Virtual Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    - name: Create T1 Cloud VM
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ t1_cloud_project_id }}"
        name: "web-server-01"
        description: "Web server instance"
        image_id: "ubuntu-20.04"
        flavor_id: "medium"
        subnet_id: "{{ subnet_id }}"
        disk_size: 50
        assign_public_ip: true
        ssh_keys:
          - "{{ ssh_public_key }}"
        state: present

Managing VM State
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    - name: Stop VM
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ t1_cloud_project_id }}"
        name: "web-server-01"
        state: stopped

    - name: Start VM
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ t1_cloud_project_id }}"
        name: "web-server-01"
        state: started

    - name: Delete VM
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ t1_cloud_project_id }}"
        name: "web-server-01"
        state: absent

Creating VM with Additional Disks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    - name: Create VM with extra storage
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ t1_cloud_project_id }}"
        name: "storage-server"
        image_id: "ubuntu-20.04"
        flavor_id: "large"
        subnet_id: "{{ subnet_id }}"
        disk_size: 50
        extra_disks:
          - name: "data-disk-1"
            size: 100
            type_name: "ssd"
          - name: "backup-disk-1"
            size: 200
            type_name: "hdd"
        state: present

Contributing to this collection
-------------------------------

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the `T1 Cloud Compute Instance collection repository`_.

Release notes
-------------

See the `changelog`_.

Roadmap
-------

* Support for additional T1 Cloud services
* Network management modules
* Storage management modules
* Load balancer management
* Auto-scaling groups

More information
----------------

- `T1 Cloud Official Website`_
- `T1 Cloud API Documentation`_
- `Ansible Collection development guide`_

.. _T1 Cloud Compute Instance collection repository: https://github.com/GRomR1/ansible-collection-t1-cloud
.. _changelog: https://github.com/GRomR1/ansible-collection-t1-cloud/blob/main/CHANGELOG.rst
.. _T1 Cloud Official Website: https://t1-cloud.ru/
.. _Ansible Collection development guide: https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html

Licensing
---------

Apache License 2.0

See `LICENSE`_ to see the full text.

.. _LICENSE: https://github.com/GRomR1/ansible-collection-t1-cloud/blob/main/LICENSE
