.. _gromr10.compute_instance.t1_cloud_iam_token_lookup:


gromr10.compute_instance.t1_cloud_iam_token lookup -- Obtain access token for T1 Cloud authentication
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Retrieves access token using service account API key
- Uses OAuth2 client credentials flow with service account
- Supports automatic token refresh and caching
- Provides secure authentication mechanism for T1 Cloud API access




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
                    <div class="ansibleOptionAnchor" id="parameter-auth_method"></div>
                    <b>auth_method</b>
                    <a class="ansibleOptionLink" href="#parameter-auth_method" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>service_account</li>
                        </ul>
                </td>
                <td>
                        <div>Authentication method to use</div>
                        <div>Currently only &#x27;service_account&#x27; is supported</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-client_id"></div>
                    <b>client_id</b>
                    <a class="ansibleOptionLink" href="#parameter-client_id" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Service account client ID (format: sa_proj-uuid)</div>
                        <div>Can be obtained from T1 Cloud console when creating API key</div>
                        <div>Required when not using key_file</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-client_secret"></div>
                    <b>client_secret</b>
                    <a class="ansibleOptionLink" href="#parameter-client_secret" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Service account client secret (API key)</div>
                        <div>Can be obtained from T1 Cloud console when creating API key</div>
                        <div>Required when not using key_file</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-key_file"></div>
                    <b>key_file</b>
                    <a class="ansibleOptionLink" href="#parameter-key_file" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Path to service account key file (JSON format)</div>
                        <div>Alternative to providing client_id and client_secret separately</div>
                        <div>File should contain client_id and client_secret fields</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-auth_url"></div>
                    <b>auth_url</b>
                    <a class="ansibleOptionLink" href="#parameter-auth_url" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"https://auth.t1.cloud/identity/oauth/token"</div>
                </td>
                <td>
                        <div>T1 Cloud OAuth2 token endpoint URL</div>
                        <div>Override only if using different endpoint</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-cache_duration"></div>
                    <b>cache_duration</b>
                    <a class="ansibleOptionLink" href="#parameter-cache_duration" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">3600</div>
                </td>
                <td>
                        <div>Token cache duration in seconds</div>
                        <div>Token will be cached to avoid unnecessary API calls</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: Get access token using client credentials
      debug:
        msg: "{{ lookup('gromr10.compute_instance.t1_cloud_iam_token',
                  auth_method='service_account',
                  client_id='sa_proj-12345678-1234-1234-1234-123456789012',
                  client_secret='your-secret-key-here') }}"

    - name: Get access token using key file
      debug:
        msg: "{{ lookup('gromr10.compute_instance.t1_cloud_iam_token',
                  auth_method='service_account',
                  key_file='/path/to/service-account.json') }}"

    - name: Use token in subsequent tasks
      set_fact:
        api_token: "{{ lookup('gromr10.compute_instance.t1_cloud_iam_token',
                       auth_method='service_account',
                       client_id=service_account_id,
                       client_secret=service_account_secret) }}"

    - name: Create VM with obtained token
      gromr10.compute_instance.t1_cloud_vm:
        api_token: "{{ api_token }}"
        project_id: "{{ project_id }}"
        name: "test-vm"
        image_id: "ubuntu-20.04"
        flavor_id: "small"
        subnet_id: "{{ subnet_id }}"
        state: present

    - name: Get token with custom auth URL
      debug:
        msg: "{{ lookup('gromr10.compute_instance.t1_cloud_iam_token',
                  auth_method='service_account',
                  client_id=service_account_id,
                  client_secret=service_account_secret,
                  auth_url='https://auth.t1.cloud/identity/oauth/token') }}"



Return Values
-------------

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-access_token"></div>
                    <b>access_token</b>
                    <a class="ansibleOptionLink" href="#return-access_token" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>JWT access token for T1 Cloud API authentication</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Notes
-----

.. note::
   - The lookup plugin automatically handles token caching to improve performance
   - Tokens are cached based on client_id to avoid conflicts between different service accounts
   - If token expires, the plugin will automatically refresh it on the next call
   - For security, avoid logging or displaying the actual token values
   - Service account credentials can be created in the T1 Cloud console under API Keys section


Status
------


Authors
~~~~~~~

- Руслан Гайнанов <rgainanov@inno.tech>


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
