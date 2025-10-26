#!/bin/bash
# Quick setup script for any module testing
# Usage: ./setup_module.sh module_name module_path [database_name]

MODULE_NAME=$1
MODULE_PATH=$2
DB_NAME=${3:-staging2}

if [ -z "$MODULE_NAME" ] || [ -z "$MODULE_PATH" ]; then
    echo "❌ Usage: ./setup_module.sh module_name module_path [database_name]"
    echo "   Example: ./setup_module.sh my_module /path/to/my_module staging2"
    exit 1
fi

if [ ! -d "$MODULE_PATH" ]; then
    echo "❌ Module path $MODULE_PATH does not exist!"
    exit 1
fi

echo "🔧 Setting up testing for module: $MODULE_NAME"
echo "📂 Module path: $MODULE_PATH"
echo "🗄️  Database: $DB_NAME"

# Create directory structure
mkdir -p "$MODULE_PATH/tests/generated_tests"
mkdir -p "$MODULE_PATH/tests/scripts"
mkdir -p "$MODULE_PATH/tests/results/view_results"
mkdir -p "$MODULE_PATH/tests/results/python_results"

# Copy and modify test scripts
cp test_script.py "$MODULE_PATH/tests/scripts/"
cp test_python_script.py "$MODULE_PATH/tests/scripts/"

# Update module configuration in copied files
sed -i "s/MODULE_NAME = \"freezoner_custom\"/MODULE_NAME = \"$MODULE_NAME\"/g" "$MODULE_PATH/tests/scripts/test_script.py"
sed -i "s|MODULE_PATH = \"/home/sabry/harbord/odoo18/phase_2/freezoner_custom\"|MODULE_PATH = \"$MODULE_PATH\"|g" "$MODULE_PATH/tests/scripts/test_python_script.py"
sed -i "s/DB_NAME = \"staging2\"/DB_NAME = \"$DB_NAME\"/g" "$MODULE_PATH/tests/scripts/test_script.py"

# Update output paths
sed -i "s|/home/sabry/harbord/odoo18/phase_2/freezoner_custom/tests|$MODULE_PATH/tests|g" "$MODULE_PATH/tests/scripts/test_script.py"
sed -i "s|/home/sabry/harbord/odoo18/phase_2/freezoner_custom/tests|$MODULE_PATH/tests|g" "$MODULE_PATH/tests/scripts/test_python_script.py"

echo "✅ Setup completed!"
echo "📁 Tests directory: $MODULE_PATH/tests"
echo ""
echo "🚀 Next steps:"
echo "1. cd $MODULE_PATH/tests/scripts"
echo "2. python3 test_script.py"
echo "3. python3 test_python_script.py"
echo "4. cd /path/to/odoo && python3 odoo-bin -c odoo.conf -d $DB_NAME --test-tags $MODULE_NAME --stop-after-init" 