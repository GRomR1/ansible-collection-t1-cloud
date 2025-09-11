# Publishing T1 Cloud Compute Instance Collection

This guide explains how to build and publish the T1 Cloud Compute Instance Ansible Collection to Ansible Galaxy.

## Prerequisites

Before publishing the collection, ensure you have:

1. **Ansible Core** installed (version 2.9.10 or higher)
   ```bash
   pip install ansible-core
   ```

2. **Ansible Galaxy account** with API token
   - Sign up at https://galaxy.ansible.com/
   - Generate API token in your profile settings

3. **Collection namespace** registered on Galaxy
   - Request the `gromr10` namespace if not already owned
   - Or use your own namespace

## Building the Collection

### 1. Validate Collection Structure

First, ensure your collection has the proper structure:

```
ansible_collections/gromr10/compute_instance/
├── galaxy.yml                 # Collection metadata
├── README.rst                 # Main documentation
├── LICENSE                    # License file
├── CHANGELOG.rst              # Version history
├── plugins/
│   ├── modules/
│   │   └── t1_cloud_vm.py
│   └── lookup/
│       └── t1_cloud_iam_token.py
├── meta/
│   └── runtime.yml
├── docs/
│   ├── t1_cloud_vm_module.rst
│   └── t1_cloud_iam_token_lookup.rst
└── examples/
    └── create_vm.yml
```

### 2. Update Version Information

Before building, update the version in:
- `galaxy.yml` - Update the `version` field
- `CHANGELOG.rst` - Add new version section

### 3. Build the Collection

Use the provided build script:

```bash
./build_collection.sh
```

Or build manually:

```bash
cd ansible_collections/gromr10/compute_instance
ansible-galaxy collection build --output-path ../../../dist --force
```

This creates a tarball in the `dist/` directory:
```
dist/gromr10-compute_instance-1.0.0.tar.gz
```

### 4. Verify the Build

Check the contents of the built collection:

```bash
tar -tzf dist/gromr10-compute_instance-1.0.0.tar.gz
```

Test the documentation:

```bash
# Install locally first
ansible-galaxy collection install dist/gromr10-compute_instance-1.0.0.tar.gz --force

# Test documentation
ansible-doc gromr10.compute_instance.t1_cloud_vm
ansible-doc -t lookup gromr10.compute_instance.t1_cloud_iam_token
```

## Publishing to Ansible Galaxy

### 1. Set Up API Token

Configure your Ansible Galaxy API token:

```bash
export ANSIBLE_GALAXY_TOKEN="your-api-token-here"
```

Or create a token file:

```bash
echo "your-api-token-here" > ~/.ansible/galaxy_token
```

### 2. Publish to Galaxy

Publish the collection:

```bash
ansible-galaxy collection publish dist/gromr10-compute_instance-1.0.0.tar.gz
```

Or with explicit token:

```bash
ansible-galaxy collection publish dist/gromr10-compute_instance-1.0.0.tar.gz --api-key your-api-token-here
```

### 3. Verify Publication

After successful publication:

1. **Check Galaxy page**: Visit https://galaxy.ansible.com/gromr10/compute_instance
2. **Install from Galaxy**:
   ```bash
   ansible-galaxy collection install gromr10.compute_instance
   ```
3. **Test installation**:
   ```bash
   ansible-doc gromr10.compute_instance.t1_cloud_vm
   ```

## Publishing to Private Galaxy

For private Galaxy servers:

```bash
ansible-galaxy collection publish dist/gromr10-compute_instance-1.0.0.tar.gz \
    --server https://your-private-galaxy.com/ \
    --api-key $ANSIBLE_GALAXY_API_KEY
```

## Version Management

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (1.X.0): New features (backward compatible)
- **PATCH** (1.0.X): Bug fixes (backward compatible)

### Release Process

1. **Update CHANGELOG.rst**:
   ```rst
   v1.1.0
   ======

   Release Summary
   ---------------
   Added support for new T1 Cloud features.

   New Features
   ------------
   - Added security groups support to t1_cloud_vm module
   - Enhanced error handling in lookup plugin

   Bugfixes
   --------
   - Fixed token refresh issue in authentication
   ```

2. **Update galaxy.yml**:
   ```yaml
   version: 1.1.0
   ```

3. **Commit and tag**:
   ```bash
   git add galaxy.yml CHANGELOG.rst
   git commit -m "Release version 1.1.0"
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin v1.1.0
   ```

4. **Build and publish**:
   ```bash
   ./build_collection.sh
   ansible-galaxy collection publish dist/gromr10-compute_instance-1.1.0.tar.gz
   ```

## Quality Checklist

Before publishing, ensure:

### Code Quality
- [ ] All Python code follows PEP 8
- [ ] No syntax errors or linting issues
- [ ] Proper error handling implemented
- [ ] Security best practices followed

### Documentation
- [ ] All modules have complete DOCUMENTATION blocks
- [ ] Examples are tested and working
- [ ] README.rst is comprehensive
- [ ] CHANGELOG.rst is up to date

### Testing
- [ ] Collection builds without errors
- [ ] ansible-doc works for all plugins
- [ ] Example playbooks execute successfully
- [ ] No broken imports or missing dependencies

### Metadata
- [ ] galaxy.yml has correct version
- [ ] License file is present
- [ ] Author information is accurate
- [ ] Tags and description are relevant
