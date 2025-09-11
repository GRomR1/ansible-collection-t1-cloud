#!/bin/bash

# Build script for T1 Cloud Compute Instance Ansible Collection
# This script builds the collection and optionally publishes it to Ansible Galaxy

set -e

# Configuration
COLLECTION_PATH="ansible_collections/gromr10/compute_instance"
BUILD_DIR="build"
DIST_DIR="dist"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "$COLLECTION_PATH" ]; then
    log_error "Collection directory not found: $COLLECTION_PATH"
    log_error "Please run this script from the project root directory"
    exit 1
fi

# Check if ansible-galaxy is available
if ! command -v ansible-galaxy &> /dev/null; then
    log_error "ansible-galaxy command not found"
    log_error "Please install Ansible (ansible-core) to build collections"
    exit 1
fi

# Clean previous builds
log_info "Cleaning previous builds..."
rm -rf "$BUILD_DIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR" "$DIST_DIR"

# Copy collection to build directory
log_info "Copying collection to build directory..."
cp -r "$COLLECTION_PATH" "$BUILD_DIR/"

# Validate collection structure
log_info "Validating collection structure..."
cd "$BUILD_DIR/compute_instance"

# Check required files
required_files=("galaxy.yml" "README.rst" "LICENSE")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        log_error "Required file missing: $file"
        exit 1
    fi
done

# Check plugins
if [ ! -d "plugins/modules" ] || [ ! -f "plugins/modules/t1_cloud_vm.py" ]; then
    log_error "Module plugins directory or t1_cloud_vm.py not found"
    exit 1
fi

if [ ! -d "plugins/lookup" ] || [ ! -f "plugins/lookup/t1_cloud_iam_token.py" ]; then
    log_error "Lookup plugins directory or t1_cloud_iam_token.py not found"
    exit 1
fi

log_success "Collection structure validation passed"

# Build the collection
log_info "Building collection..."
ansible-galaxy collection build --output-path "../../$DIST_DIR" --force

cd ../..

# List built artifacts
log_info "Built artifacts:"
ls -la "$DIST_DIR"

# Get the built collection filename
COLLECTION_FILE=$(ls "$DIST_DIR"/gromr10-compute_instance-*.tar.gz 2>/dev/null | head -1)

if [ -z "$COLLECTION_FILE" ]; then
    log_error "No collection tarball found in $DIST_DIR"
    exit 1
fi

log_success "Collection built successfully: $(basename "$COLLECTION_FILE")"

# Verify the collection
log_info "Verifying collection contents..."
tar -tzf "$COLLECTION_FILE" | head -20

echo
log_info "Collection build completed successfully!"
log_info "Collection file: $COLLECTION_FILE"

# Installation instructions
echo
echo "To install the built collection locally:"
echo "  ansible-galaxy collection install $COLLECTION_FILE"
echo
echo "To publish to Ansible Galaxy (requires API token):"
echo "  ansible-galaxy collection publish $COLLECTION_FILE --api-key $ANSIBLE_GALAXY_API_KEY"
echo
echo "To publish to a private Galaxy server:"
echo "  ansible-galaxy collection publish $COLLECTION_FILE --server https://your-galaxy-server.com/"

# Optional: Install locally for testing
read -p "Would you like to install the collection locally for testing? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Installing collection locally..."
    ansible-galaxy collection install "$COLLECTION_FILE" --force
    log_success "Collection installed successfully!"

    echo
    log_info "You can now test the collection with:"
    echo "  ansible-doc gromr10.compute_instance.t1_cloud_vm"
    echo "  ansible-doc -t lookup gromr10.compute_instance.t1_cloud_iam_token"
fi

echo
log_success "Build process completed!"
