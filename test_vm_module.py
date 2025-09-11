#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for t1_cloud_vm Ansible module.
This script tests the basic functionality of the module without actually running Ansible.
"""

import sys
import os
import json
# Add the module path to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'plugins', 'modules'))

try:
    from plugins.modules.t1_cloud_vm import T1CloudVM, build_vm_config, validate_name
    from plugins.lookup.t1_cloud_iam_token import T1CloudAuth
    print("✓ Module imports successfully")
except ImportError as e:
    print(f"✗ Failed to import module: {e}")
    sys.exit(1)

def test_vm_name_validation():
    """Test VM name validation function"""
    print("\n--- Testing VM name validation ---")

    valid_names = [
        "test-vm",
        "my-server-01",
        "web-app-backend",
        "db-cluster-1",
        "a1-b2-c3"
    ]

    invalid_names = [
        "Test-VM",  # uppercase
        "a",  # too short
        "vm_with_underscore",  # underscore not allowed
        "very-long-name-that-exceeds-the-maximum-allowed-length-for-vm-names-in-t1-cloud"  # too long
    ]

    for name in valid_names:
        if validate_name(name):
            print(f"✓ '{name}' is valid")
        else:
            print(f"✗ '{name}' should be valid but validation failed")

    for name in invalid_names:
        if not validate_name(name):
            print(f"✓ '{name}' correctly identified as invalid")
        else:
            print(f"✗ '{name}' should be invalid but validation passed")

def test_vm_config_builder():
    """Test VM configuration builder"""
    print("\n--- Testing VM configuration builder ---")

    # Mock module parameters
    class MockModule:
        def __init__(self):
            self.params = {
                'name': 'test-vm',
                'description': 'Test virtual machine',
                'image_id': 'd0179cb4-bfad-4b8f-836f-9cfc02143560',
                'image_name': '',
                'flavor_id': '3b259b39-6e73-41d5-b98e-b93c0bf31e95',
                'flavor_name': '',
                'region_id': '0c530dd3-eaae-4216-8f9d-9b5710a7cc30',
                'region_name': 'ru-central1',
                'availability_zone_id': 'd3p1k01',
                'availability_zone_name': 'ru-central1-a',
                'disk_size': 30,
                'disk_type_id': '7ced5dc4-848a-4c02-bb76-8a3a9b7fff7f',
                'disk_type_name': 'POD2_Average',
                'extra_disks': [],
                'network_id': '',
                'subnet_id': 'd0a5e4c0-1323-483d-8f5a-0e797a0fdd85',
                'subnet_cidr': '10.9.60.0/24',
                'subnet_name': '10-9-60-0-24',
                'assign_public_ip': False,
                'create_public_ip': True,
                'public_ip_bandwidth': 1000,
                'requested_ip': '',
                'security_groups': ['3706eb85-cb97-4713-a581-3ed76cb745d3'],
                'ssh_keys': [],
                'user_data': '',
                'preemptible': False,
                'labels': {'environment': 'test', 'team': 'devops'}
            }

    mock_module = MockModule()

    try:
        config = build_vm_config(mock_module)
        print("✓ VM configuration built successfully")

        # Check required fields
        required_fields = ['name', 'description', 'region', 'availability_zone',
                          'image', 'flavor', 'volumes_config', 'network_configuration']

        for field in required_fields:
            if field in config:
                print(f"✓ Required field '{field}' present")
            else:
                print(f"✗ Required field '{field}' missing")

        # Check labels
        if 'labels' in config and config['labels'] == mock_module.params['labels']:
            print("✓ Labels correctly set")
        else:
            print("✗ Labels not set correctly")

    except Exception as e:
        print(f"✗ Failed to build VM configuration: {e}")

def test_t1cloud_client_initialization():
    """Test T1CloudVM client initialization"""
    print("\n--- Testing T1CloudVM client initialization ---")

    try:
        # Test with dummy credentials
        client = T1CloudVM(
            api_token="dummy_token",
            project_id="proj-test123"
        )
        print("✓ T1CloudVM client initialized successfully")

        # Check if base attributes are set correctly
        if client.api_token == "dummy_token":
            print("✓ API token set correctly")
        else:
            print("✗ API token not set correctly")

        if client.project_id == "proj-test123":
            print("✓ Project ID set correctly")
        else:
            print("✗ Project ID not set correctly")

        if client.base_url == "https://api.t1.cloud":
            print("✓ Base URL set correctly")
        else:
            print("✗ Base URL not set correctly")

    except Exception as e:
        print(f"✗ Failed to initialize T1CloudVM client: {e}")

def test_vm_config_with_extra_disks():
    """Test VM configuration with additional disks"""
    print("\n--- Testing VM configuration with extra disks ---")

    class MockModuleWithDisks:
        def __init__(self):
            self.params = {
                'name': 'vm-with-disks',
                'description': 'VM with additional storage',
                'image_id': 'd0179cb4-bfad-4b8f-836f-9cfc02143560',
                'image_name': '',
                'flavor_id': '3b259b39-6e73-41d5-b98e-b93c0bf31e95',
                'flavor_name': '',
                'region_id': '0c530dd3-eaae-4216-8f9d-9b5710a7cc30',
                'region_name': 'ru-central1',
                'availability_zone_id': 'd3p1k01',
                'availability_zone_name': 'ru-central1-a',
                'disk_size': 50,
                'disk_type_id': '7ced5dc4-848a-4c02-bb76-8a3a9b7fff7f',
                'disk_type_name': 'POD2_Average',
                'extra_disks': [
                    {
                        'name': 'data-disk',
                        'size': 100,
                        'type_id': 'cb4724f6-e53e-4632-ac78-f83c4332add3',
                        'type_name': 'ceph_hdd'
                    },
                    {
                        'name': 'logs-disk',
                        'size': 50,
                        'type_id': '7ced5dc4-848a-4c02-bb76-8a3a9b7fff7f',
                        'type_name': 'POD2_Average'
                    }
                ],
                'network_id': '',
                'subnet_id': 'd0a5e4c0-1323-483d-8f5a-0e797a0fdd85',
                'subnet_cidr': '10.9.60.0/24',
                'subnet_name': '10-9-60-0-24',
                'assign_public_ip': True,
                'create_public_ip': True,
                'public_ip_bandwidth': 2000,
                'requested_ip': '',
                'security_groups': [],
                'ssh_keys': ['key1', 'key2'],
                'user_data': '#cloud-config\nusers:\n  - name: admin',
                'preemptible': False,
                'labels': {}
            }

    mock_module = MockModuleWithDisks()

    try:
        config = build_vm_config(mock_module)
        print("✓ VM configuration with extra disks built successfully")

        # Check extra volumes
        if 'volumes_config' in config and 'extra_volumes' in config['volumes_config']:
            extra_volumes = config['volumes_config']['extra_volumes']
            if len(extra_volumes) == 2:
                print("✓ Extra volumes configured correctly")

                # Check first disk
                if extra_volumes[0]['name'] == 'data-disk' and extra_volumes[0]['size'] == 100:
                    print("✓ First extra disk configured correctly")
                else:
                    print("✗ First extra disk not configured correctly")

                # Check second disk
                if extra_volumes[1]['name'] == 'logs-disk' and extra_volumes[1]['size'] == 50:
                    print("✓ Second extra disk configured correctly")
                else:
                    print("✗ Second extra disk not configured correctly")
            else:
                print(f"✗ Expected 2 extra volumes, got {len(extra_volumes)}")
        else:
            print("✗ Extra volumes not configured")

        # Check public IP configuration
        if config.get('add_public_ip') and config.get('create_public_ip'):
            print("✓ Public IP configuration set correctly")
        else:
            print("✗ Public IP configuration not set correctly")

        # Check SSH keys
        if config.get('ssh_keys') == ['key1', 'key2']:
            print("✓ SSH keys configured correctly")
        else:
            print("✗ SSH keys not configured correctly")

        # Check user data
        if config.get('add_user_data') and config.get('user_data'):
            print("✓ User data configured correctly")
        else:
            print("✗ User data not configured correctly")

    except Exception as e:
        print(f"✗ Failed to build VM configuration with extra disks: {e}")

def test_vm_runtime_info_parsing():
    """Test parsing of runtime information from API responses"""
    print("\n--- Testing VM runtime info parsing ---")

    try:
        T1CloudVM(
            api_token="dummy_token",
            project_id="proj-test123"
        )
        print("✓ T1CloudVM client created for runtime info testing")

        # Mock compute instance response (similar to actual API response)
        mock_instance_response = {
            "data": {
                "state": "on",
                "config": {
                    "id": "14a0cc6f-c8da-4dc2-80f6-b370637d6f1c",
                    "name": "test-vm",
                    "description": "Test VM for runtime info",
                    "addresses": {
                        "10-9-60-0-24": [
                            {
                                "addr": "10.9.60.20",
                                "version": 4,
                                "OS-EXT-IPS:type": "fixed",
                                "OS-EXT-IPS-MAC:mac_addr": "02:78:a5:7d:97:16"
                            }
                        ]
                    },
                    "accessIPv4": "10.9.60.20",
                    "accessIPv6": "",
                    "flavor": {
                        "id": "3b259b39-6e73-41d5-b98e-b93c0bf31e95",
                        "name": "b5.large.2",
                        "vcpus": 2,
                        "ram": 4096
                    },
                    "source_image": {
                        "id": "d0179cb4-bfad-4b8f-836f-9cfc02143560",
                        "name": "osmax-astra-1-7-5-orel-gui-2025-05-19",
                        "os_distro": "astra"
                    },
                    "availability_zone": {
                        "id": "d3p1k01",
                        "name": "ru-central1-a"
                    }
                }
            },
            "order_id": "15b92322-144f-4eec-9746-0d830f61647d",
            "item_id": "14a0cc6f-c8da-4dc2-80f6-b370637d6f1c",
            "created_row_dt": "2025-09-01T07:08:41.810562"
        }

        # Test the runtime info extraction logic
        config = mock_instance_response["data"]["config"]
        runtime_info = {
            'instance_id': config.get('id'),
            'name': config.get('name'),
            'status': mock_instance_response["data"].get('state'),
            'power_status': mock_instance_response["data"].get('state'),
            'primary_ipv4': config.get('accessIPv4', ''),
            'primary_ipv6': config.get('accessIPv6', ''),
            'ip_addresses': {},
            'flavor': config.get('flavor', {}),
            'image': config.get('source_image', {}),
            'availability_zone': config.get('availability_zone', {})
        }

        # Extract IP addresses
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

        # Verify parsed data
        if runtime_info['instance_id'] == "14a0cc6f-c8da-4dc2-80f6-b370637d6f1c":
            print("✓ Instance ID extracted correctly")
        else:
            print("✗ Instance ID not extracted correctly")

        if runtime_info['name'] == "test-vm":
            print("✓ VM name extracted correctly")
        else:
            print("✗ VM name not extracted correctly")

        if runtime_info['power_status'] == "on":
            print("✓ Power status extracted correctly")
        else:
            print("✗ Power status not extracted correctly")

        if runtime_info['primary_ipv4'] == "10.9.60.20":
            print("✓ Primary IPv4 extracted correctly")
        else:
            print("✗ Primary IPv4 not extracted correctly")

        if '10-9-60-0-24' in runtime_info['ip_addresses']:
            network_ips = runtime_info['ip_addresses']['10-9-60-0-24']
            if len(network_ips) == 1 and network_ips[0]['addr'] == "10.9.60.20":
                print("✓ Network IP addresses extracted correctly")
            else:
                print("✗ Network IP addresses not extracted correctly")
        else:
            print("✗ Network IP addresses not found")

        if runtime_info['flavor']['name'] == "b5.large.2" and runtime_info['flavor']['vcpus'] == 2:
            print("✓ Flavor information extracted correctly")
        else:
            print("✗ Flavor information not extracted correctly")

        if runtime_info['image']['os_distro'] == "astra":
            print("✓ Image information extracted correctly")
        else:
            print("✗ Image information not extracted correctly")

        if runtime_info['availability_zone']['name'] == "ru-central1-a":
            print("✓ Availability zone extracted correctly")
        else:
            print("✗ Availability zone not extracted correctly")

    except Exception as e:
        print(f"✗ Failed to test runtime info parsing: {e}")

def test_vm_creation():
    """Test VM creation"""
    print("\n--- Testing VM creation ---")

    # Mock module parameters
    class MockModule:
        def __init__(self):
            self.params = {
                'name': 'test-vm',
                'description': 'Test virtual machine',

                'region_id': '0c530dd3-eaae-4216-8f9d-9b5710a7cc30',
                'region_name': 'ru-central1',

                'availability_zone_id': 'd3p1k01',
                'availability_zone_name': 'ru-central1-a',

                'flavor_id': '3b259b39-6e73-41d5-b98e-b93c0bf31e95',
                'flavor_name': 'b5.large.2',
                'flavor_ram': 4096,
                'flavor_vcpus': 2,

                'image_id': "cc20ce19-d35e-49b7-8c80-144ac044250a",

                'disk_size': 30,
                'disk_type_id': '7ced5dc4-848a-4c02-bb76-8a3a9b7fff7f',
                'disk_type_name': 'POD2_Average',
                'extra_disks': [],

                'network_id': '',
                'subnet_id': 'd0a5e4c0-1323-483d-8f5a-0e797a0fdd85',
                'subnet_cidr': '10.9.60.0/24',
                'subnet_name': '10-9-60-0-24',
                'toggle_shared_network': False,
                'assign_public_ip': False,
                'create_public_ip': False,
                'requested_ip': '',

                'security_groups': ['3706eb85-cb97-4713-a581-3ed76cb745d3'],
                'ssh_keys': [],
                'preemptible': False,
                'user_data': '#cloud-config\nusers:\n  - name: admin',

                'labels': {'environment': 'test', 'team': 'devops'}
            }

    mock_module = MockModule()

    try:
        config = build_vm_config(mock_module)
        print(f"VM Configuration:\n{json.dumps(config, indent=4, ensure_ascii=False)}")

        auth_client = T1CloudAuth()
        token_info = auth_client.get_token_with_credentials(
          client_id=os.environ.get('T1_CLOUD_CLIENT_ID'),
          client_secret=os.environ.get('T1_CLOUD_CLIENT_SECRET')
        )
        if not token_info or 'access_token' not in token_info:
            raise Exception("Failed to obtain access token")
        access_token = token_info['access_token']

        client = T1CloudVM(
            api_token=access_token,
            project_id=os.environ.get('T1_CLOUD_PROJECT_ID'),
        )
        response = client.create_vm(config)
        print(f"Response:\n{json.dumps(response, indent=4, ensure_ascii=False)}")
        order_id = response.pop().get('id')
        print(f"VM created with ID: {order_id}")
        final_order = client.wait_for_operation(order_id)
        print(f"Final order:\n{json.dumps(final_order, indent=4, ensure_ascii=False)}")

    except Exception as e:
        print(f"✗ Failed to create VM: {e}")

def main():
    """Run all tests"""
    print("T1 Cloud VM Module Test Suite")
    print("=" * 40)

    test_vm_name_validation()
    test_vm_config_builder()
    test_t1cloud_client_initialization()
    test_vm_config_with_extra_disks()
    test_vm_runtime_info_parsing()
    # test_vm_creation() # uncomment only when you need to test actual API calls

    print("\n" + "=" * 40)
    print("Test suite completed!")
    print("\nNote: These tests only check module structure and configuration building.")
    print("To test actual API calls, you need valid T1.Cloud credentials and a real project.")


if __name__ == '__main__':
    main()
