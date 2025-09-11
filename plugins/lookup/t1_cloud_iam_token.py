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
    name: t1_cloud_iam_token
    author: T1 Cloud Module Contributors
    version_added: "1.0.0"
    short_description: Obtain access token for T1 Cloud authentication
    description:
        - Retrieves access token using service account API key
        - Uses OAuth2 client credentials flow with service account
        - Supports automatic token refresh and caching
    options:
        auth_method:
            description:
                - Authentication method to use
                - Currently only 'service_account' is supported
            required: true
            type: str
            choices: ['service_account']
        client_id:
            description:
                - Service account client ID (format: sa_proj-uuid)
                - Can be obtained from T1 Cloud console when creating API key
            required: false
            type: str
        client_secret:
            description:
                - Service account client secret (API key)
                - Can be obtained from T1 Cloud console when creating API key
            required: false
            type: str
        key_file:
            description:
                - Path to service account key file (JSON format)
                - Should contain client_id and client_secret fields
                - Alternative to providing client_id and client_secret directly
            required: false
            type: str
        endpoint:
            description:
                - T1 Cloud authorization endpoint URL
            required: false
            type: str
            default: "https://auth.t1.cloud/auth/realms/Portal/protocol/openid-connect/token"
        scope:
            description:
                - OAuth2 scope for token request
            required: false
            type: str
            default: "openid"
        grant_type:
            description:
                - OAuth2 grant type
            required: false
            type: str
            default: "client_credentials"
    requirements:
        - python >= 3.6
        - requests
    notes:
        - Service account API keys can be created in T1 Cloud console
        - Access tokens are valid for 1 hour
        - Tokens are automatically refreshed when expired
'''

EXAMPLES = r'''
# Get access token using client_id and client_secret
- name: Get access token with credentials
  debug:
    msg: "{{ lookup('t1_cloud_iam_token', 'service_account', client_id='sa_proj-12345678-1234-1234-1234-123456789012', client_secret='your_secret_key') }}"

# Get access token using service account key file
- name: Get access token with key file
  debug:
    msg: "{{ lookup('t1_cloud_iam_token', 'service_account', key_file='/path/to/service_account.json') }}"

# Use token in T1 Cloud modules
- name: Create VM with token
  t1_cloud_vm:
    api_token: "{{ lookup('t1_cloud_iam_token', 'service_account', key_file='/path/to/service_account.json') }}"
    project_id: "proj-xxxxxxxxxx"
    name: "test-vm"
    # ... other parameters

# Example service account key file format:
# {
#   "client_id": "sa_proj-12345678-1234-1234-1234-123456789012",
#   "client_secret": "your_secret_key_here",
#   "type": "service_account",
#   "project_id": "proj-xxxxxxxxxx"
# }
'''

RETURN = r'''
_raw:
    description: Access token for API authentication
    type: str
    returned: success
token_type:
    description: Type of the token (usually "Bearer")
    type: str
    returned: success
expires_in:
    description: Token expiration time in seconds
    type: int
    returned: success
'''

import json
from datetime import datetime, timedelta
from urllib.parse import urlencode

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()


class T1CloudAuth:
    """
    Class for obtaining access tokens from T1 Cloud authorization service.

    :param endpoint: T1 Cloud authorization endpoint URL
    :type endpoint: str
    """

    def __init__(self, endpoint="https://auth.t1.cloud/auth/realms/Portal/protocol/openid-connect/token"):
        """
        Initialize T1CloudAuth instance.

        :param endpoint: Authorization service endpoint URL
        :type endpoint: str
        """
        self.endpoint = endpoint
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        })
        # Token cache to avoid unnecessary requests
        self._token_cache = {}

    def _is_token_expired(self, token_info):
        """
        Check if cached token is expired.

        :param token_info: Token information dictionary
        :type token_info: dict
        :return: True if token is expired, False otherwise
        :rtype: bool
        """
        if not token_info or 'expires_at' not in token_info:
            return True

        # Add 5 minute buffer before actual expiration
        buffer_time = 300  # 5 minutes
        return datetime.now() >= (token_info['expires_at'] - timedelta(seconds=buffer_time))

    def get_token_with_credentials(self, client_id, client_secret, scope="openid", grant_type="client_credentials"):
        """
        Get access token using service account credentials.

        :param client_id: Service account client ID
        :type client_id: str
        :param client_secret: Service account client secret
        :type client_secret: str
        :param scope: OAuth2 scope
        :type scope: str
        :param grant_type: OAuth2 grant type
        :type grant_type: str
        :return: Access token information
        :rtype: dict
        :raises: Exception if token retrieval fails
        """
        # Check cache first
        cache_key = f"{client_id}:{scope}:{grant_type}"
        if cache_key in self._token_cache:
            cached_token = self._token_cache[cache_key]
            if not self._is_token_expired(cached_token):
                display.vvv(f"Using cached token for client_id: {client_id}")
                return cached_token

        try:
            # Prepare request data
            data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': grant_type,
                'scope': scope
            }

            display.vvv(f"Requesting token for client_id: {client_id}")

            response = self.session.post(
                self.endpoint,
                data=urlencode(data),
                timeout=30
            )
            response.raise_for_status()

            result = response.json()

            if 'access_token' not in result:
                raise Exception("No access_token in response")

            # Prepare token info
            token_info = {
                'access_token': result['access_token'],
                'token_type': result.get('token_type', 'Bearer'),
                'expires_in': result.get('expires_in', 3600),
                'scope': result.get('scope', scope),
                'expires_at': datetime.now() + timedelta(seconds=result.get('expires_in', 3600))
            }

            # Cache the token
            self._token_cache[cache_key] = token_info

            display.vvv(f"Successfully obtained token, expires in {token_info['expires_in']} seconds")
            return token_info

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {e.response.status_code}"
            try:
                error_details = e.response.json()
                if 'error_description' in error_details:
                    error_msg += f": {error_details['error_description']}"
                elif 'error' in error_details:
                    error_msg += f": {error_details['error']}"
            except:
                error_msg += f": {e.response.text}"
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get access token: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing token request: {str(e)}")

    def get_token_from_file(self, key_file_path, scope="openid", grant_type="client_credentials"):
        """
        Get access token using service account key file.

        :param key_file_path: Path to service account key file
        :type key_file_path: str
        :param scope: OAuth2 scope
        :type scope: str
        :param grant_type: OAuth2 grant type
        :type grant_type: str
        :return: Access token information
        :rtype: dict
        :raises: Exception if token retrieval fails
        """
        try:
            # Read service account key file
            with open(key_file_path, 'r', encoding='utf-8') as f:
                key_data = json.load(f)

            # Extract required fields
            client_id = key_data.get('client_id')
            client_secret = key_data.get('client_secret')

            if not client_id or not client_secret:
                raise Exception("Service account key file must contain 'client_id' and 'client_secret' fields")

            # Validate client_id format
            if not client_id.startswith('sa_proj-'):
                display.warning(f"Client ID format may be incorrect: {client_id}. Expected format: sa_proj-<uuid>")

            return self.get_token_with_credentials(client_id, client_secret, scope, grant_type)

        except FileNotFoundError:
            raise Exception(f"Service account key file not found: {key_file_path}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON in service account key file: {key_file_path}")
        except Exception as e:
            if "Service account key file" in str(e) or "client_id" in str(e):
                raise
            raise Exception(f"Error reading service account key file: {str(e)}")


class LookupModule(LookupBase):
    """
    Ansible lookup plugin for T1 Cloud access tokens.
    """

    def run(self, terms, variables=None, **kwargs): # type: ignore
        """
        Main lookup method.

        :param terms: Lookup terms (auth method)
        :type terms: list
        :param variables: Ansible variables
        :type variables: dict or None
        :param kwargs: Additional keyword arguments
        :type kwargs: dict
        :return: List containing access token
        :rtype: list
        :raises: AnsibleError if lookup fails
        """
        if not HAS_REQUESTS:
            raise AnsibleError("The 'requests' library is required for this lookup plugin")

        if not terms:
            raise AnsibleError("t1_cloud_iam_token lookup requires authentication method")

        auth_method = terms[0]

        if auth_method not in ['service_account']:
            raise AnsibleError(f"Invalid authentication method: {auth_method}. Only 'service_account' is supported.")

        # Get parameters
        client_id = kwargs.get('client_id')
        client_secret = kwargs.get('client_secret')
        key_file = kwargs.get('key_file')
        endpoint = kwargs.get('endpoint', 'https://auth.t1.cloud/auth/realms/Portal/protocol/openid-connect/token')
        scope = kwargs.get('scope', 'openid')
        grant_type = kwargs.get('grant_type', 'client_credentials')

        # Validate input parameters
        if not key_file and (not client_id or not client_secret):
            raise AnsibleError(
                "Either 'key_file' parameter or both 'client_id' and 'client_secret' parameters are required"
            )

        if key_file and (client_id or client_secret):
            raise AnsibleError(
                "Use either 'key_file' parameter or 'client_id'/'client_secret' parameters, not both"
            )

        try:
            auth_client = T1CloudAuth(endpoint=endpoint)

            if key_file:
                display.vvv(f"Getting access token using service account key file: {key_file}")
                token_info = auth_client.get_token_from_file(key_file, scope, grant_type)
            else:
                display.vvv(f"Getting access token using client credentials: {client_id}")
                token_info = auth_client.get_token_with_credentials(client_id, client_secret, scope, grant_type)

            if not token_info or 'access_token' not in token_info:
                raise AnsibleError("Failed to obtain access token")

            display.vvv("Successfully obtained access token")
            return [token_info['access_token']]

        except Exception as e:
            raise AnsibleError(f"T1 Cloud access token lookup failed: {str(e)}")
