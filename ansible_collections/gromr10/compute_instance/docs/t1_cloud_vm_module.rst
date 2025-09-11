.. _gromr10.compute_instance.t1_cloud_vm_module:


gromr10.compute_instance.t1_cloud_vm module -- Manage virtual machines in T1 Cloud
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Create, delete, start, stop, and manage virtual machines in T1 Cloud using REST API.
- Supports full VM lifecycle management including disk configuration and network setup.
- Manages VM resources such as CPU, RAM, storage volumes, and network interfaces.
- Supports cloud-init user data and SSH key injection for VM initialization.
- Provides comprehensive state management for production workloads.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-api_token"></div>
                    <b>api_token</b>
                    <a class="ansibleOptionLink" href="#parameter-api_token" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>T1 Cloud API token for authentication.</div>
                        <div>Can be obtained from T1 Cloud console.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-project_id"></div>
                    <b>project_id</b>
                    <a class="ansibleOptionLink" href="#parameter-project_id" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The ID of the project where VM should be created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-name"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the virtual machine.</div>
                        <div>Must be unique within the project.</div>
                        <div>Must match pattern ^[a-z][a-z0-9-]{1,61}[a-z0-9]$.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-description"></div>
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-description" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Description of the virtual machine.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-image_id"></div>
                    <b>image_id</b>
                    <a class="ansibleOptionLink" href="#parameter-image_id" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Operating system image ID or name.</div>
                        <div>Required when state=present.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-flavor_id"></div>
                    <b>flavor_id</b>
                    <a class="ansibleOptionLink" href="#parameter-flavor_id" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VM flavor ID or name defining CPU and RAM resources.</div>
                        <div>Required when state=present.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-subnet_id"></div>
                    <b>subnet_id</b>
                    <a class="ansibleOptionLink" href="#parameter-subnet_id" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Subnet ID where VM should be connected.</div>
                        <div>Required when state=present.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-disk_size"></div>
                    <b>disk_size</b>
                    <a class="ansibleOptionLink" href="#parameter-disk_size" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">20</div>
                </td>
                <td>
                        <div>Size of the boot disk in GB.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-extra_disks"></div>
                    <b>extra_disks</b>
                    <a class="ansibleOptionLink" href="#parameter-extra_disks" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of additional disks to attach to the VM.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-assign_public_ip"></div>
                    <b>assign_public_ip</b>
                    <a class="ansibleOptionLink" href="#parameter-assign_public_ip" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>false</b>&nbsp;&larr;</div></li>
                                    <li>true</li>
                        </ul>
                </td>
                <td>
                        <div>Whether to assign a public IP address to the VM.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-ssh_keys"></div>
                    <b>ssh_keys</b>
                    <a class="ansibleOptionLink" href="#parameter-ssh_keys" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of SSH public keys to inject into the VM.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-user_data"></div>
                    <b>user_data</b>
                    <a class="ansibleOptionLink" href="#parameter-user_data" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Cloud-init user data for VM initialization.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-labels"></div>
                    <b>labels</b>
                    <a class="ansibleOptionLink" href="#parameter-labels" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Key-value pairs for labeling the VM.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-state"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                                    <li>started</li>
                                    <li>stopped</li>
                        </ul>
                </td>
                <td>
                        <div>Desired state of the virtual machine.</div>
                        <div>present - create VM if it doesn't exist</div>
                        <div>absent - delete VM if it exists</div>
                        <div>started - start VM if it's stopped</div>
                        <div>stopped - stop VM if it's running</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: Create a simple VM
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ project_id }}"
        name: "test-vm"
        description: "Test virtual machine"
        image_id: "ubuntu-20.04"
        flavor_id: "small"
        subnet_id: "{{ subnet_id }}"
        disk_size: 20
        state: present

    - name: Create VM with additional disks and public IP
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ project_id }}"
        name: "web-server"
        description: "Web server with storage"
        image_id: "ubuntu-20.04"
        flavor_id: "medium"
        subnet_id: "{{ subnet_id }}"
        disk_size: 50
        extra_disks:
          - name: "data-disk"
            size: 100
            type_name: "ssd"
        assign_public_ip: true
        ssh_keys:
          - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAB..."
        labels:
          environment: "production"
          service: "web"
        state: present

    - name: Stop VM
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ project_id }}"
        name: "web-server"
        state: stopped

    - name: Start VM
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ project_id }}"
        name: "web-server"
        state: started

    - name: Delete VM
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ t1_cloud_api_token }}"
        project_id: "{{ project_id }}"
        name: "web-server"
        state: absent



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-vm"></div>
                    <b>vm</b>
                    <a class="ansibleOptionLink" href="#return-vm" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>Information about the VM order</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{
    "id": "12345",
    "status": "active",
    "created_at": "2023-01-15T10:30:00Z",
    "updated_at": "2023-01-15T10:35:00Z",
    "attrs": {
        "name": "test-vm",
        "description": "Test virtual machine",
        "image": {
            "id": "ubuntu-20.04",
            "name": "Ubuntu 20.04",
            "os_distro": "ubuntu"
        },
        "flavor": {
            "id": "small",
            "name": "Small",
            "vcpus": 1,
            "ram": 2048
        },
        "volumes_config": {
            "boot_volume": {
                "size": 20,
                "volume_type": {
                    "name": "ssd"
                }
            }
        }
    }
}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-order_id"></div>
                    <b>order_id</b>
                    <a class="ansibleOptionLink" href="#return-order_id" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>ID of the created/modified order</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">67890</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-changed"></div>
                    <b>changed</b>
                    <a class="ansibleOptionLink" href="#return-changed" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Whether the VM state was changed</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- T1 Cloud Module Contributors


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
