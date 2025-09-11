Contributing to T1 Cloud Compute Instance Collection
====================================================

We welcome contributions to the T1 Cloud Compute Instance Ansible Collection! This guide will help you get started with development and contribution.

.. contents:: Topics


Development Environment Setup
-----------------------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.8 or higher
- Ansible Core 2.9.10 or higher
- Git
- A T1 Cloud account with API access

Setting up the Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Clone the repository:**

   .. code-block:: bash

       git clone https://github.com/GRomR1/ansible-collection-t1-cloud.git
       cd ansible-collection-compute-instance

2. **Create a virtual environment:**

   .. code-block:: bash

       python -m venv .venv
       source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install dependencies:**

   .. code-block:: bash

       pip install ansible-core
       pip install -r requirements.txt

4. **Install the collection in development mode:**

   .. code-block:: bash

       ansible-galaxy collection install -p ~/.ansible/collections .

5. **Set up environment variables for testing:**

   .. code-block:: bash

       export T1_CLOUD_PROJECT_ID="xxxxxxx"
       export T1_CLOUD_CLIENT_ID="sa_proj-xxxxxxxxx"
       export T1_CLOUD_CLIENT_SECRET="xxxxxxx"

Testing
-------

Running Tests
~~~~~~~~~~~~~

Before submitting any changes, ensure all tests pass:

.. code-block:: bash

    # Validate collection structure
    ansible-galaxy collection build --force

    # Test module documentation
    ansible-doc gromr10.compute_instance.t1_cloud_vm
    ansible-doc -t lookup gromr10.compute_instance.t1_cloud_iam_token

    # Run integration tests (requires T1 Cloud credentials)
    ansible-playbook ansible_collections/gromr10/compute_instance/examples/create_vm.yml --check --syntax-check

Manual Testing
~~~~~~~~~~~~~~

1. **Test module functionality:**

   .. code-block:: bash

       ansible -m gromr10.compute_instance.t1_cloud_vm localhost \
           -a "api_token=$T1_CLOUD_API_TOKEN project_id=$T1_CLOUD_PROJECT_ID \
               name=test-vm image_id=ubuntu-20.04 flavor_id=small \
               subnet_id=$T1_CLOUD_SUBNET_ID state=present"

2. **Test lookup plugin:**

   .. code-block:: bash

       ansible localhost -m debug \
           -a "msg={{ lookup('gromr10.compute_instance.t1_cloud_iam_token',
                      auth_method='service_account',
                      client_id='your-client-id',
                      client_secret='your-client-secret') }}"

Code Style and Standards
------------------------

Python Code Standards
~~~~~~~~~~~~~~~~~~~~~~

- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Use type hints where appropriate

.. code-block:: python

    def create_vm(self, vm_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a virtual machine with the specified configuration.

        Args:
            vm_config: Dictionary containing VM configuration parameters

        Returns:
            Dictionary containing VM creation result

        Raises:
            T1CloudAPIError: If API request fails
        """

Documentation Standards
~~~~~~~~~~~~~~~~~~~~~~~

- All modules must have comprehensive DOCUMENTATION blocks
- Include examples for common use cases
- Document all parameters and return values
- Use proper reStructuredText formatting

.. code-block:: python

    DOCUMENTATION = r'''
    ---
    module: t1_cloud_vm
    short_description: Manage virtual machines in T1 Cloud
    description:
        - Create, delete, start, stop, and manage virtual machines in T1 Cloud
        - Supports full VM lifecycle management
    options:
        api_token:
            description: T1 Cloud API token for authentication
            required: true
            type: str
            no_log: true
    '''

Commit Message Format
~~~~~~~~~~~~~~~~~~~~~

Use conventional commit format:

.. code-block:: text

    <type>(<scope>): <description>

    <body>

    <footer>

Types:
- ``feat``: New feature
- ``fix``: Bug fix
- ``docs``: Documentation changes
- ``style``: Code style changes
- ``refactor``: Code refactoring
- ``test``: Adding or updating tests
- ``chore``: Maintenance tasks

Examples:

.. code-block:: text

    feat(vm): add support for custom security groups

    - Added security_groups parameter to t1_cloud_vm module
    - Updated documentation and examples
    - Added validation for security group IDs

    Closes #123

    fix(lookup): handle token expiration correctly

    Fixed issue where expired tokens were not refreshed automatically

    Fixes #456

Contribution Workflow
---------------------

1. **Fork the repository** on GitHub

2. **Create a feature branch:**

   .. code-block:: bash

       git checkout -b feature/your-feature-name

3. **Make your changes** following the coding standards

4. **Test your changes** thoroughly

5. **Commit your changes:**

   .. code-block:: bash

       git add .
       git commit -m "feat(module): add new functionality"

6. **Push to your fork:**

   .. code-block:: bash

       git push origin feature/your-feature-name

7. **Create a Pull Request** on GitHub

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

- Provide a clear description of the changes
- Include test results
- Update documentation if necessary
- Reference related issues
- Ensure all CI checks pass

Adding New Modules
------------------

When adding new modules to the collection:

1. **Create the module file** in ``plugins/modules/``
2. **Follow the existing code structure** and patterns
3. **Add comprehensive documentation** in the DOCUMENTATION block
4. **Include examples** in the EXAMPLES block
5. **Define return values** in the RETURNS block
6. **Update the README.rst** to list the new module
7. **Create documentation** in the ``docs/`` directory
8. **Add examples** to the ``examples/`` directory

Module Template
~~~~~~~~~~~~~~~

.. code-block:: python

    #!/usr/bin/python
    # -*- coding: utf-8 -*-

    # Licensed under the Apache License, Version 2.0

    from __future__ import (absolute_import, division, print_function)
    __metaclass__ = type

    DOCUMENTATION = r'''
    ---
    module: t1_cloud_new_module
    short_description: Brief description
    # ... rest of documentation
    '''

    EXAMPLES = r'''
    - name: Example usage
      gromr10.compute_instance.t1_cloud_new_module:
        # ... parameters
    '''

    RETURN = r'''
    result:
        description: Description of return value
        type: dict
        returned: always
    '''

Adding New Lookup Plugins
--------------------------

For new lookup plugins:

1. **Create the plugin file** in ``plugins/lookup/``
2. **Inherit from LookupBase**
3. **Implement the run() method**
4. **Add proper error handling**
5. **Update documentation**

Release Process
---------------

Version Numbering
~~~~~~~~~~~~~~~~~

We follow `Semantic Versioning <https://semver.org/>`_:

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

Creating a Release
~~~~~~~~~~~~~~~~~~

1. **Update version** in ``galaxy.yml``
2. **Update CHANGELOG.rst** with new version details
3. **Create a git tag:**

   .. code-block:: bash

       git tag -a v1.1.0 -m "Release version 1.1.0"
       git push origin v1.1.0

4. **Build and publish** the collection:

   .. code-block:: bash

       ./build_collection.sh
       ansible-galaxy collection publish dist/gromr10-compute_instance-*.tar.gz

Reporting Issues
----------------

When reporting issues:

1. **Check existing issues** to avoid duplicates
2. **Use the issue template** if available
3. **Provide detailed information:**
   - Ansible version
   - Collection version
   - Operating system
   - Complete error messages
   - Steps to reproduce

4. **Include relevant code** or playbook excerpts
5. **Sanitize sensitive information** (API tokens, IDs, etc.)

Getting Help
------------

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **T1 Cloud Support**: For T1 Cloud platform-specific issues

Contact Information
-------------------

- **GitHub**: https://github.com/GRomR1/ansible-collection-t1-cloud

Thank You
---------

We appreciate all contributions to make this collection better for the entire community!
