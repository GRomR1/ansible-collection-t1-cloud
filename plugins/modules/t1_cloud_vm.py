#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: t1_cloud_vm

short_description: Manage virtual machines in T1 Cloud

version_added: "1.0.0"

description:
    - Create, delete, start, stop, and manage virtual machines in T1 Cloud using REST API.
    - Supports full VM lifecycle management including disk configuration and network setup.

options:
    api_token:
        description:
            - T1 Cloud API token for authentication.
            - Can be obtained from T1 Cloud console.
        required: true
        type: str
        no_log: true
    project_id:
        description:
            - The ID of the project where VM should be created.
        required: true
        type: str
    name:
        description:
            - Name of the virtual machine.
            - Must be unique within the project.
            - Must match pattern ^[a-z][a-z0-9-]{1,61}[a-z0-9]$.
        required: true
        type: str
    description:
        description:
            - Description of the virtual machine.
        required: false
        type: str
        default: ""
    image_id:
        description:
            - ID of the image to use for VM creation.
            - Required when state is present.
            - Mutually exclusive with image_name.
        required: false
        type: str
    image_name:
        description:
            - Name of the image to use for VM creation.
            - Required when state is present.
            - Mutually exclusive with image_id.
        required: false
        type: str
    flavor_id:
        description:
            - ID of the flavor (VM configuration) to use.
            - Required when state is present.
            - Mutually exclusive with flavor_name.
        required: false
        type: str
    flavor_name:
        description:
            - Name of the flavor (VM configuration) to use.
            - Required when state is present.
            - Mutually exclusive with flavor_id.
        required: false
        type: str
    flavor_ram:
        description:
            - RAM capacity in MB
        required: false
        type: int
    flavor_vcpus:
        description:
            - Number of processors
        required: false
        type: int
    region_id:
        description:
            - ID of the region where VM should be created.
        required: false
        type: str
        default: "0c530dd3-eaae-4216-8f9d-9b5710a7cc30"
    region_name:
        description:
            - Name of the region where VM should be created.
        required: false
        type: str
        default: "ru-central1"
    availability_zone_id:
        description:
            - ID of the availability zone where VM should be created.
        required: false
        type: str
        default: "d3p1k01"
    availability_zone_name:
        description:
            - Name of the availability zone where VM should be created.
        required: false
        type: str
        default: "ru-central1-a"
    disk_size:
        description:
            - Size of the boot disk in GB.
        required: false
        type: int
        default: 10
    disk_type_id:
        description:
            - ID of the disk type to use.
        required: false
        type: str
        default: "076482c0-0367-4dee-a16f-2c6673a97f7f"
    disk_type_name:
        description:
            - Name of the disk type to use.
        required: false
        type: str
        default: "POD2_Average"
    extra_disks:
        description:
            - List of additional disks to attach to VM.
            - Each disk should be a dictionary with name, size, and type.
        required: false
        type: list
        elements: dict
        default: []
    network_id:
        description:
            - ID of the network to connect VM to.
            - Required when state is present.
        required: false
        type: str
    subnet_id:
        description:
            - ID of the subnet to connect VM to.
            - Required when state is present.
        required: false
        type: str
    subnet_cidr:
        description:
            - CIDR of the subnet.
        required: false
        type: str
        default: "10.128.0.0/24"
    subnet_name:
        description:
            - Name of the subnet.
        required: false
        type: str
        default: "default-ru-central1-a"
    assign_public_ip:
        description:
            - Whether to assign public IP to VM.
        required: false
        type: bool
        default: false
    toggle_shared_network:
        description:
            - Specify true if you want to connect the server to a subnet of another project (not the one in which the server is ordered)
        required: false
        type: bool
        default: false
    create_public_ip:
        description:
            - Whether to create new public IP or use existing one.
            - Only used when assign_public_ip is true.
        required: false
        type: bool
        default: false
    public_ip_bandwidth:
        description:
            - Bandwidth limit for public IP in Mbps.
            - Only used when assign_public_ip and create_public_ip are true.
            - Must be multiple of 100, from 100 to 10000.
        required: false
        type: int
        default: 1000
    requested_ip:
        description:
            - Specific internal IP address to assign to VM.
            - If not specified, IP will be assigned automatically.
        required: false
        type: str
    security_groups:
        description:
            - List of security group IDs to apply to VM.
        required: false
        type: list
        elements: str
        default: []
    ssh_keys:
        description:
            - List of SSH key IDs to add to VM.
            - Used for Linux VMs.
        required: false
        type: list
        elements: str
        default: []
    user_data:
        description:
            - Cloud-init user data script.
            - Maximum 16384 bytes.
        required: false
        type: str
        default: ""
    preemptible:
        description:
            - Whether VM should be preemptible (may be stopped after 24h).
        required: false
        type: bool
        default: false
    labels:
        description:
            - Key-value labels to assign to VM.
        required: false
        type: dict
        default: {}
    state:
        description:
            - Desired state of the VM.
        required: false
        type: str
        choices: ['present', 'absent', 'started', 'stopped']
        default: 'present'
    wait:
        description:
            - Whether to wait for operation to complete.
        required: false
        type: bool
        default: true
    wait_timeout:
        description:
            - Maximum time to wait for operation completion in seconds.
        required: false
        type: int
        default: 600
    gather_info:
        description:
            - Whether to gather runtime information about the VM (IP addresses, power status, etc.).
            - Uses compute instances API to get current VM state.
        required: false
        type: bool
        default: true

author:
    - T1 Cloud Module Contributors

requirements:
    - python >= 3.6
    - requests
'''

EXAMPLES = r'''
# Create a simple VM with Astra Linux
- name: Create VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-gxvcuy3t6kg5vrf"
    name: "test-vm"
    description: "Test virtual machine"
    image_id: "d0179cb4-bfad-4b8f-836f-9cfc02143560"
    flavor_id: "3b259b39-6e73-41d5-b98e-b93c0bf31e95"
    subnet_id: "d0a5e4c0-1323-483d-8f5a-0e797a0fdd85"
    disk_size: 30
    disk_type_id: "7ced5dc4-848a-4c02-bb76-8a3a9b7fff7f"
    assign_public_ip: false
    ssh_keys:
      - "b5dba483-b46e-4d7f-9278-1e4fec84b6cb"
    security_groups:
      - "3706eb85-cb97-4713-a581-3ed76cb745d3"
    state: present
    wait: true
    wait_timeout: 600
    gather_info: true
  register: vm_result

- name: Display VM IP addresses
  debug:
    msg:
      - "VM created successfully!"
      - "Primary IPv4: {{ vm_result.runtime_info.primary_ipv4 | default('Not assigned') }}"
      - "All IP addresses: {{ vm_result.runtime_info.ip_addresses | default({}) }}"

# Create VM with additional disks and public IP
- name: Create VM with extra disks
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-gxvcuy3t6kg5vrf"
    name: "vm-with-disks"
    description: "VM with additional storage"
    image_id: "d0179cb4-bfad-4b8f-836f-9cfc02143560"
    flavor_id: "3b259b39-6e73-41d5-b98e-b93c0bf31e95"
    subnet_id: "d0a5e4c0-1323-483d-8f5a-0e797a0fdd85"
    disk_size: 50
    extra_disks:
      - name: "data-disk"
        size: 100
        type_id: "cb4724f6-e53e-4632-ac78-f83c4332add3"
        type_name: "ceph_hdd"
      - name: "logs-disk"
        size: 50
        type_id: "7ced5dc4-848a-4c02-bb76-8a3a9b7fff7f"
        type_name: "POD2_Average"
    assign_public_ip: true
    create_public_ip: true
    public_ip_bandwidth: 1000
    user_data: |
      #cloud-config
      users:
        - name: admin
          sudo: ALL=(ALL) NOPASSWD:ALL
          ssh_authorized_keys:
            - ssh-rsa AAAAB3NzaC1yc2E...
    labels:
      environment: "production"
      team: "devops"
      project: "web-app"
    state: present

# Start stopped VM
- name: Start VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-gxvcuy3t6kg5vrf"
    name: "test-vm"
    state: started
    wait: true

# Stop running VM
- name: Stop VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-gxvcuy3t6kg5vrf"
    name: "test-vm"
    state: stopped
    wait: true

# Delete VM
- name: Delete VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-gxvcuy3t6kg5vrf"
    name: "test-vm"
    state: absent
    wait: true

# Create VM with specific IP address
- name: Create VM with fixed IP
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-gxvcuy3t6kg5vrf"
    name: "fixed-ip-vm"
    description: "VM with predefined IP"
    image_id: "d0179cb4-bfad-4b8f-836f-9cfc02143560"
    flavor_id: "3b259b39-6e73-41d5-b98e-b93c0bf31e95"
    subnet_id: "d0a5e4c0-1323-483d-8f5a-0e797a0fdd85"
    requested_ip: "10.9.60.100"
    disk_size: 30
    state: present

# Create preemptible VM (may be stopped after 24h)
- name: Create preemptible VM
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-gxvcuy3t6kg5vrf"
    name: "preemptible-vm"
    description: "Cost-effective preemptible VM"
    image_id: "d0179cb4-bfad-4b8f-836f-9cfc02143560"
    flavor_id: "3b259b39-6e73-41d5-b98e-b93c0bf31e95"
    subnet_id: "d0a5e4c0-1323-483d-8f5a-0e797a0fdd85"
    disk_size: 20
    preemptible: true
    state: present

# Get detailed information about existing VM
- name: Get VM runtime information
  t1_cloud_vm:
    api_token: "{{ t1_api_token }}"
    project_id: "proj-gxvcuy3t6kg5vrf"
    name: "test-vm"
    state: present
    gather_info: true
  register: vm_info

- name: Display detailed VM information
  debug:
    msg:
      - "VM Status: {{ vm_info.vm.status }}"
      - "Power State: {{ vm_info.runtime_info.power_status | default('unknown') }}"
      - "Instance ID: {{ vm_info.runtime_info.instance_id | default('N/A') }}"
      - "Primary IP: {{ vm_info.runtime_info.primary_ipv4 | default('N/A') }}"
      - "All Networks: {{ vm_info.runtime_info.ip_addresses.keys() | list }}"
'''

RETURN = r'''
vm:
    description: Information about the VM order
    type: dict
    returned: always
    sample: {
        "id": "15b92322-144f-4eec-9746-0d830f61647d",
        "created_at": "2025-09-01T10:08:11+03:00",
        "updated_at": "2025-09-06T12:03:44+03:00",
        "status": "success",
        "label": "Виртуальная машина",
        "category": "instance",
        "category_v2": "compute-instance",
        "deletable": true,
        "project_name": "proj-gxvcuy3t6kg5vrf",
        "product_id": "e6fa78c9-2ee1-4f9e-b86c-5d7246f38526",
        "product_name": "compute_instance",
        "attrs": {
            "name": "test-vm",
            "description": "Test virtual machine",
            "image": {
                "id": "d0179cb4-bfad-4b8f-836f-9cfc02143560",
                "name": "osmax-astra-1-7-5-orel-gui-2025-05-19",
                "os_distro": "astra",
                "os_version": "1.7.5 Орёл"
            },
            "flavor": {
                "id": "3b259b39-6e73-41d5-b98e-b93c0bf31e95",
                "name": "b5.large.2",
                "ram": 4096,
                "vcpus": 2,
                "gpus": 0
            },
            "availability_zone": {
                "id": "d3p1k01",
                "name": "ru-central1-a"
            },
            "volumes_config": {
                "boot_volume": {
                    "size": 30,
                    "volume_type": {
                        "id": "7ced5dc4-848a-4c02-bb76-8a3a9b7fff7f",
                        "name": "POD2_Average"
                    }
                }
            },
            "network_configuration": {
                "subnet": {
                    "id": "d0a5e4c0-1323-483d-8f5a-0e797a0fdd85",
                    "cidr": "10.9.60.0/24",
                    "name": "10-9-60-0-24"
                }
            },
            "preview_items": []
        }
    }
order_id:
    description: ID of the order created/modified
    type: str
    returned: when operation creates an order
    sample: "15b92322-144f-4eec-9746-0d830f61647d"
runtime_info:
    description: Runtime information about the VM instance
    type: dict
    returned: when VM exists and compute instance API is available
    sample: {
        "instance_id": "14a0cc6f-c8da-4dc2-80f6-b370637d6f1c",
        "name": "test-vm",
        "status": "on",
        "power_status": "on",
        "description": "Test virtual machine",
        "primary_ipv4": "10.9.60.20",
        "primary_ipv6": "",
        "ip_addresses": {
            "10-9-60-0-24": [
                {
                    "addr": "10.9.60.20",
                    "version": 4,
                    "type": "fixed",
                    "mac_addr": "02:78:a5:7d:97:16"
                }
            ]
        },
        "flavor": {
            "id": "3b259b39-6e73-41d5-b98e-b93c0bf31e95",
            "name": "b5.large.2",
            "vcpus": 2,
            "ram": 4096
        },
        "availability_zone": {
            "id": "d3p1k01",
            "name": "ru-central1-a"
        }
    }
changed:
    description: Whether the VM state was changed
    type: bool
    returned: always
'''

import time
import re
import json
from urllib.parse import urljoin

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None

from ansible.module_utils.basic import AnsibleModule


class T1CloudVM:
    """
    Class for managing T1 Cloud VMs via REST API.

    :param api_token: T1 Cloud API token
    :type api_token: str
    :param project_id: Project ID where VM should be managed
    :type project_id: str
    """

    def __init__(self, api_token, project_id, base_url="https://api.t1.cloud"):
        """
        Initialize T1CloudVM instance.

        :param api_token: T1 Cloud API token for authentication
        :type api_token: str
        :param project_id: Project ID where VM operations will be performed
        :type project_id: str
        """
        self.api_token = api_token
        self.project_id = project_id
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'ansible-t1-cloud/1.0.0'
        }

        if requests is not None:
            self.session = requests.Session()
            self.session.headers.update(self.headers)

            # Configure retry strategy
            from requests.adapters import HTTPAdapter
            from urllib3.util import Retry

            retry_strategy = Retry(
                total=3,
                status_forcelist=[429, 500, 502, 503, 504],
                backoff_factor=1
            )

            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)
        else:
            raise Exception("requests library is required")

    def _make_request(self, method, endpoint, data=None, params=None, timeout=30):
        """
        Make HTTP request to T1 Cloud API.

        :param method: HTTP method (GET, POST, DELETE, etc.)
        :type method: str
        :param endpoint: API endpoint path
        :type endpoint: str
        :param data: Request body data
        :type data: dict or None
        :param params: URL query parameters
        :type params: dict or None
        :return: Response object or None
        :rtype: requests.Response or None
        """
        url = urljoin(self.base_url, endpoint)

        try:
            if requests is None:
                raise Exception("requests library is not available")

            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e: # type: ignore
            response_json = None
            if isinstance(e.response, requests.Response): # type: ignore
              try:
                  response_json = e.response.json()
                  error_message = response_json.get('message', response.text)
              except (ValueError, json.JSONDecodeError):
                  error_message = response.text or f"HTTP {response.status_code}"
            raise Exception(f"API request failed: {str(e)}\n Error message:{str(error_message)}")

    def get_vm_by_name(self, name):
        """
        Get VM information by name.

        :param name: VM name to search for
        :type name: str
        :return: VM information or None if not found
        :rtype: dict or None
        """
        endpoint = f"/order-service/api/v1/projects/{self.project_id}/orders"
        params = {
            "per_page": 100,
            "f[product_name][]": "compute_instance"
        }

        response = self._make_request('GET', endpoint, params=params)
        if response and response.status_code == 200:
            data = response.json()
            orders = data.get('list', [])
            for order in orders:
                if order.get('attrs', {}).get('name') == name:
                    return order
        return None

    def get_vm_by_id(self, vm_id):
        """
        Get VM information by ID.

        :param vm_id: VM ID to search for
        :type vm_id: str
        :return: VM information or None if not found
        :rtype: dict or None
        """
        endpoint = f"/order-service/api/v1/projects/{self.project_id}/orders/{vm_id}"

        response = self._make_request('GET', endpoint)
        if response and response.status_code == 200:
            return response.json()
        return None

    def create_vm(self, vm_config):
        """
        Create a new virtual machine.

        :param vm_config: VM configuration dictionary
        :type vm_config: dict
        :return: Created VM information
        :rtype: dict
        """
        endpoint = f"/order-service/api/v1/projects/{self.project_id}/orders"

        order_data = {
            "order": {
                "project_name": f"{self.project_id}",
                "product_name": "compute_instance",
                "product_id": "e6fa78c9-2ee1-4f9e-b86c-5d7246f38526",  # OpenStack VM product ID
                "count": 1,
                "attrs": vm_config
            }
        }

        response = self._make_request('POST', endpoint, data=order_data)
        if response and response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Failed to create VM: {response.text if response else 'No response'}")

    def delete_vm(self, vm_id):
        """
        Delete a virtual machine.

        :param vm_id: ID of the VM to delete
        :type vm_id: str
        :return: Deletion operation result
        :rtype: dict
        """
        vm_order = self.get_vm_by_id(vm_id)
        if not vm_order:
            raise Exception(f"VM with ID {vm_id} not found")

        item_id = self.get_vm_instance_item_id(vm_order)
        if not item_id:
            raise Exception(f"Could not find instance item_id for VM {vm_id}")

        return self.execute_vm_action(vm_id, item_id, "compute_instance_delete")

    def wait_for_operation(self, order_id, timeout=600):
        """
        Wait for operation to complete.

        :param order_id: ID of the order to wait for
        :type order_id: str
        :param timeout: Maximum time to wait in seconds
        :type timeout: int
        :return: Final operation status
        :rtype: dict
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            endpoint = f"/order-service/api/v1/projects/{self.project_id}/orders/{order_id}"
            response = self._make_request('GET', endpoint)

            if response and response.status_code == 200:
                order = response.json()
                status = order.get('status', 'unknown')

                if status in ['success', 'failure', 'creation_error', 'validation_error']:
                    return order
                elif status in ['deprovisioned', 'deprovisioned_error']:
                    return order

            time.sleep(10)  # Wait 10 seconds before next check

        raise Exception(f"Operation timeout after {timeout} seconds")

    def get_vm_status(self, vm_id):
        """
        Get current VM status.

        :param vm_id: VM ID to check
        :type vm_id: str
        :return: VM status information
        :rtype: dict
        """
        endpoint = f"/order-service/api/v1/projects/{self.project_id}/compute/instances/{vm_id}"

        response = self._make_request('GET', endpoint)
        if response and response.status_code == 200:
            return response.json()
        return None

    def get_vm_instances(self, filters=None):
        """
        Get list of VM instances from compute service.

        :param filters: Optional filters for the request
        :type filters: dict or None
        :return: List of VM instances or None
        :rtype: list or None
        """
        endpoint = f"/order-service/api/v1/projects/{self.project_id}/compute/instances"
        params = filters or {}

        response = self._make_request('GET', endpoint, params=params)
        if response and response.status_code == 200:
            data = response.json()
            return data.get('list', [])
        return None

    def get_vm_instance_by_id(self, instance_id, with_actions=True, with_children=False):
        """
        Get detailed VM instance information by ID.

        :param instance_id: VM instance ID
        :type instance_id: str
        :param with_actions: Include available actions
        :type with_actions: bool
        :param with_children: Include child resources
        :type with_children: bool
        :return: VM instance details or None
        :rtype: dict or None
        """
        endpoint = f"/order-service/api/v1/projects/{self.project_id}/compute/instances/{instance_id}"
        params = {
            "with_actions": str(with_actions).lower(),
            "with_children": str(with_children).lower()
        }

        response = self._make_request('GET', endpoint, params=params)
        if response and response.status_code == 200:
            return response.json()
        return None

    def get_vm_instance_by_name(self, name):
        """
        Get VM instance information by name from compute service.

        :param name: VM name to search for
        :type name: str
        :return: VM instance information or None
        :rtype: dict or None
        """
        instances = self.get_vm_instances({"name": name})
        if instances:
            for instance in instances:
                if instance.get('data', {}).get('config', {}).get('name') == name:
                    return instance
        return None

    def get_vm_runtime_info(self, vm_name_or_id):
        """
        Get comprehensive runtime information about VM including IP addresses,
        power status, and other dynamic parameters.

        :param vm_name_or_id: VM name or instance ID
        :type vm_name_or_id: str
        :return: Dictionary with runtime information
        :rtype: dict
        """
        # First try to get by name from compute instances
        instance = self.get_vm_instance_by_name(vm_name_or_id)

        # If not found by name, try as instance ID
        if not instance:
            instance = self.get_vm_instance_by_id(vm_name_or_id)

        if not instance:
            return None

        config = instance.get('data', {}).get('config', {})

        # Extract runtime information
        runtime_info = {
            'instance_id': config.get('id'),
            'name': config.get('name'),
            'status': instance.get('data', {}).get('state', 'unknown'),
            'power_status': instance.get('data', {}).get('state', 'unknown'),
            'description': config.get('description', ''),
            'created_at': instance.get('created_row_dt'),
            'order_id': instance.get('order_id'),
            'item_id': instance.get('item_id'),
            'ip_addresses': {},
            'flavor': config.get('flavor', {}),
            'image': config.get('source_image', {}),
            'availability_zone': config.get('availability_zone', {}),
            'volumes': [],
            'network_interfaces': []
        }

        # Extract IP addresses from addresses field
        addresses = config.get('addresses', {})
        for network_name, ips in addresses.items():
            runtime_info['ip_addresses'][network_name] = []
            for ip_info in ips:
                ip_data = {
                    'addr': ip_info.get('addr'),
                    'version': ip_info.get('version'),
                    'type': ip_info.get('OS-EXT-IPS:type'),
                    'mac_addr': ip_info.get('OS-EXT-IPS-MAC:mac_addr')
                }
                runtime_info['ip_addresses'][network_name].append(ip_data)

        # Extract primary IP addresses
        runtime_info['primary_ipv4'] = config.get('accessIPv4', '')
        runtime_info['primary_ipv6'] = config.get('accessIPv6', '')

        return runtime_info

    def get_vm_instance_item_id(self, vm_order):
        """
        Get instance item_id from VM order.

        :param vm_order: VM order data
        :type vm_order: dict
        :return: Instance item_id or None
        :rtype: str or None
        """
        preview_items = vm_order.get('attrs', {}).get('preview_items', [])
        for item in preview_items:
            if item.get('type') == 'instance':
                return item.get('item_id')
        return None

    def execute_vm_action(self, vm_id, item_id, action_name, attrs=None):
        """
        Execute action on VM.

        :param vm_id: VM order ID
        :type vm_id: str
        :param item_id: VM instance item ID
        :type item_id: str
        :param action_name: Action to execute
        :type action_name: str
        :param attrs: Additional attributes for action
        :type attrs: dict or None
        :return: Action result
        :rtype: dict
        """
        endpoint = f"/order-service/api/v1/projects/{self.project_id}/orders/{vm_id}/actions/{action_name}"

        action_data = {
            "item_id": item_id,
            "order": {
                "attrs": attrs or {}
            }
        }

        response = self._make_request('PATCH', endpoint, data=action_data)
        if response and response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Failed to execute action '{action_name}': {response.text if response else 'No response'}")

    def start_vm(self, vm_id):
        """
        Start a virtual machine.

        :param vm_id: ID of the VM to start
        :type vm_id: str
        :return: Operation result
        :rtype: dict
        """
        vm_order = self.get_vm_by_id(vm_id)
        if not vm_order:
            raise Exception(f"VM with ID {vm_id} not found")

        item_id = self.get_vm_instance_item_id(vm_order)
        if not item_id:
            raise Exception(f"Could not find instance item_id for VM {vm_id}")

        return self.execute_vm_action(vm_id, item_id, "start_compute_vm")

    def stop_vm(self, vm_id):
        """
        Stop a virtual machine.

        :param vm_id: ID of the VM to stop
        :type vm_id: str
        :return: Operation result
        :rtype: dict
        """
        vm_order = self.get_vm_by_id(vm_id)
        if not vm_order:
            raise Exception(f"VM with ID {vm_id} not found")

        item_id = self.get_vm_instance_item_id(vm_order)
        if not item_id:
            raise Exception(f"Could not find instance item_id for VM {vm_id}")

        return self.execute_vm_action(vm_id, item_id, "stop_compute_vm")


def build_vm_config(module):
    """
    Build VM configuration from module parameters.

    :param module: Ansible module instance
    :type module: AnsibleModule
    :return: VM configuration dictionary
    :rtype: dict
    """
    params = module.params

    config = {
        "name": params['name'],
        "description": params['description'],
        "region": {
            "id": params['region_id'],
            "name": params['region_name'],
            "description": ""
        },
        "availability_zone": {
            "id": params['availability_zone_id'],
            "name": params['availability_zone_name'],
            "description": ""
        }
    }

    # Image configuration
    if params['image_id']:
        config["image"] = {
            "id": params['image_id'],
            "name": params.get('image_name', ''),
            "os_distro": "windows",
        }
    elif params['image_name']:
        # In real implementation, we would need to look up image ID by name
        config["image"] = {
            "id": "",  # Would be resolved by API call
            "name": params['image_name'],
            "os_distro": "windows",
        }

    # Flavor configuration
    if params['flavor_id']:
        config["flavor"] = {
            "id": params['flavor_id'],
            "name": params.get('flavor_name', ''),
            "ram": params.get('flavor_ram', 4096),  # Default values
            "vcpus": params.get('flavor_vcpus', 2),  # Default values
            "gpus": 0
        }
    elif params['flavor_name']:
        config["flavor"] = {
            "id": "",  # Would be resolved by API call
            "name": params['flavor_name'],
            "ram": params.get('flavor_ram', 4096),  # Default values
            "vcpus": params.get('flavor_vcpus', 2),  # Default values
            "gpus": 0
        }

    config["volumes_config"] = {}
    # Disk configuration
    config["volumes_config"] = {
        "boot_volume": {
            "size": params['disk_size'],
            "volume_type": {
                "id": params['disk_type_id'],
                "name": params['disk_type_name'],
                "extra_specs": {}
            }
        },
        "extra_volumes": []
    }

    # Extra disks
    if params['extra_disks']:
        config["volumes_config"]["extra_volumes"] = []
        for disk in params['extra_disks']:
            extra_disk = {
                "name": disk.get('name', 'extra-disk'),
                "size": disk['size'],
                "volume_type": {
                    "id": disk.get('type_id', 'cb4724f6-e53e-4632-ac78-f83c4332add3'),
                    "name": disk.get('type_name', 'ceph_hdd'),
                    "extra_specs": {}
                }
            }
            config["volumes_config"]["extra_volumes"].append(extra_disk)

    # Network configuration
    config["network_configuration"] = {
        "subnet": {
            "id": params['subnet_id'],
            "cidr": params['subnet_cidr'],
            "name": params['subnet_name']
        },
        "set_ip_address": bool(params['requested_ip']),
        "toggle_shared_network": bool(params['toggle_shared_network'])
    }

    if params['requested_ip']:
        config["network_configuration"]["requested_ip"] = params['requested_ip']

    # Public IP configuration
    config["add_public_ip"] = params['assign_public_ip']
    if params['assign_public_ip']:
        config["create_public_ip"] = params['create_public_ip']
        if params['create_public_ip']:
            config["public_ip_bandwidth"] = params['public_ip_bandwidth']

    # Security groups
    if params['security_groups']:
        config["security_groups"] = [
            {"id": sg_id, "name": "default"} for sg_id in params['security_groups']
        ]

    # SSH keys
    if params['ssh_keys']:
        config["ssh_keys"] = params['ssh_keys']

    # User data
    config["add_user_data"] = bool(params['user_data'])
    if params['user_data']:
        config["user_data"] = params['user_data']

    # Other settings
    config["preemptible"] = params['preemptible']
    config["add_placement_policy"] = False

    # Add labels if provided
    if params['labels']:
        config["labels"] = params['labels']

    return config


def validate_name(name):
    """
    Validate VM name according to T1 Cloud requirements.

    :param name: VM name to validate
    :type name: str
    :return: True if valid, False otherwise
    :rtype: bool
    """
    pattern = r'^[a-z0-9-]{1,61}$'
    return bool(re.match(pattern, name))


def main():
    """
    Main module execution function.
    """
    if not HAS_REQUESTS:
        raise ImportError("The 'requests' library is required for this module")

    argument_spec = dict(
        api_token=dict(type='str', required=True, no_log=True),
        project_id=dict(type='str', required=True),
        name=dict(type='str', required=True),
        description=dict(type='str', default=''),
        image_id=dict(type='str', default=''),
        image_name=dict(type='str', default=''),
        flavor_id=dict(type='str'),
        flavor_name=dict(type='str'),
        flavor_ram=dict(type='int'),   # Объём оперативной памяти в МБ
        flavor_vcpus=dict(type='int'), # Количество процессоров
        region_id=dict(type='str', default='0c530dd3-eaae-4216-8f9d-9b5710a7cc30'),
        region_name=dict(type='str', default='ru-central1'),
        availability_zone_id=dict(type='str', default='d3p1k01'),
        availability_zone_name=dict(type='str', default='ru-central1-a'),
        disk_size=dict(type='int', default=10),
        disk_type_id=dict(type='str', default='076482c0-0367-4dee-a16f-2c6673a97f7f'),
        disk_type_name=dict(type='str', default='POD2_Average'),
        extra_disks=dict(type='list', elements='dict', default=[]),
        network_id=dict(type='str'),
        subnet_id=dict(type='str'),
        subnet_cidr=dict(type='str', default='10.128.0.0/24'),
        subnet_name=dict(type='str', default='default-ru-central1-a'),
        toggle_shared_network=dict(type='bool', default=False),
        assign_public_ip=dict(type='bool', default=False),
        create_public_ip=dict(type='bool', default=False),
        public_ip_bandwidth=dict(type='int', default=1000),
        requested_ip=dict(type='str', default=''),
        security_groups=dict(type='list', elements='str', default=[]),
        ssh_keys=dict(type='list', elements='str', default=[]),
        user_data=dict(type='str', default=''),
        preemptible=dict(type='bool', default=False),
        labels=dict(type='dict', default={}),
        state=dict(type='str', choices=['present', 'absent', 'started', 'stopped'], default='present'),
        wait=dict(type='bool', default=True),
        wait_timeout=dict(type='int', default=600),
        gather_info=dict(type='bool', default=True)
    )

    required_if = [
        ('state', 'present', ['project_id', 'name']),
    ]

    mutually_exclusive = [
        ['image_id', 'image_name'],
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True
    )

    # Validate VM name
    if not validate_name(module.params['name']):
        module.fail_json(
            msg=f"Invalid VM name '{module.params['name']}'. "
                "Name must match pattern: ^[a-z0-9-]{{1,61}}$"
        )

    # Validate bandwidth
    if module.params['assign_public_ip'] and module.params['create_public_ip']:
        bandwidth = module.params['public_ip_bandwidth']
        if bandwidth < 100 or bandwidth > 10000 or bandwidth % 100 != 0:
            module.fail_json(
                msg="public_ip_bandwidth must be between 100 and 10000 and multiple of 100"
            )

    # Validate user_data size
    if len(module.params['user_data']) > 16384:
        module.fail_json(msg="user_data cannot exceed 16384 bytes")

    try:
        client = T1CloudVM(
            api_token=module.params['api_token'],
            project_id=module.params['project_id']
        )

        result = {
            'changed': False,
            'vm': {},
            'order_id': None
        }

        vm_name = module.params['name']
        current_vm = client.get_vm_by_name(vm_name)

        if module.params['state'] == 'present':
            if current_vm:
                # VM exists, check if update needed
                result['vm'] = current_vm
                result['changed'] = False
            else:
                # Create new VM
                if not module.check_mode:
                    vm_config = build_vm_config(module)
                    response = client.create_vm(vm_config)
                    result['order_id'] = response.pop().get('id')

                    if module.params['wait']:
                        final_order = client.wait_for_operation(
                            result['order_id'],
                            module.params['wait_timeout']
                        )
                        result['vm'] = final_order
                    else:
                        result['vm'] = response

                result['changed'] = True

        elif module.params['state'] == 'absent':
            if current_vm:
                if not module.check_mode:
                    client.delete_vm(current_vm['id'])
                result['changed'] = True
            else:
                result['changed'] = False

        elif module.params['state'] in ['started', 'stopped']:
            if not current_vm:
                module.fail_json(msg=f"VM '{vm_name}' not found")

            vm_id = current_vm.get('id')
            if not vm_id:
                module.fail_json(msg=f"Could not get VM ID for '{vm_name}'")

            # Get current VM status from compute instances API for accurate runtime info
            runtime_info = client.get_vm_runtime_info(vm_name)
            current_power_state = 'unknown'

            if runtime_info:
                current_power_state = runtime_info.get('power_status', 'unknown')
                # Add runtime information to result
                result['runtime_info'] = runtime_info
            else:
                # Fallback to order data if compute API unavailable
                if 'attrs' in current_vm and 'preview_items' in current_vm['attrs']:
                    for item in current_vm['attrs']['preview_items']:
                        if item.get('type') == 'instance':
                            current_power_state = item.get('data', {}).get('state', 'unknown')
                            break

            if module.params['state'] == 'started':
                if current_power_state == 'off':
                    if not module.check_mode:
                        action_result = client.start_vm(vm_id)
                        if module.params['wait']:
                            client.wait_for_operation(action_result.get('id', vm_id), module.params['wait_timeout'])
                    result['changed'] = True
                else:
                    result['changed'] = False
            elif module.params['state'] == 'stopped':
                if current_power_state == 'on':
                    if not module.check_mode:
                        action_result = client.stop_vm(vm_id)
                        if module.params['wait']:
                            client.wait_for_operation(action_result.get('id', vm_id), module.params['wait_timeout'])
                    result['changed'] = True
                else:
                    result['changed'] = False

            result['vm'] = current_vm

        # Get runtime information if requested and VM exists
        if result.get('vm') and module.params.get('gather_info', True) and not result.get('runtime_info'):
            try:
                runtime_info = client.get_vm_runtime_info(vm_name)
                if runtime_info:
                    result['runtime_info'] = runtime_info
            except Exception:
                # Don't fail if runtime info unavailable, just continue
                pass

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"T1 Cloud API error: {str(e)}")

if __name__ == '__main__':
    main()
