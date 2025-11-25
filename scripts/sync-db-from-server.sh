#!/bin/bash
# Sync database from deployment server to local development
# Usage: ./scripts/sync-db-from-server.sh [environment]
#   environment: 'homelab' or 'production' (default: interactive)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

DEPLOY_ENV=${1}

# Interactive environment selection if not provided
if [ -z "$DEPLOY_ENV" ]; then
    echo "Select environment to sync from:"
    echo "  [1] testing (default)"
    echo "  [2] production"
    read -p "Enter number [1]: " choice

    case ${choice:-1} in
        1) DEPLOY_ENV="testing" ;;
        2) DEPLOY_ENV="production" ;;
        *) echo "Invalid choice. Defaulting to testing."; DEPLOY_ENV="testing" ;;
    esac
fi

echo ""
echo "========================================="
echo "Database Sync from ${DEPLOY_ENV}"
echo "========================================="
echo ""
echo "This will:"
echo "  1. Dump database from ${DEPLOY_ENV} server"
echo "  2. DESTROY your local database"
echo "  3. Restore the remote database locally"
echo ""
read -p "Continue? [y/N]: " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Check if ansible is available
if ! command -v ansible-playbook &> /dev/null; then
    echo ""
    echo "ERROR: ansible-playbook not found. Please install Ansible first."
    echo "  brew install ansible  # macOS"
    echo "  pip install ansible   # Python"
    exit 1
fi

# Check if inventory file exists
INVENTORY_FILE="infrastructure/hosts.ini"
if [ ! -f "$INVENTORY_FILE" ]; then
    echo ""
    echo "ERROR: Inventory file not found: $INVENTORY_FILE"
    echo "Make sure you're running this from the project root."
    exit 1
fi

echo ""
echo "→ Step 1: Dumping database from ${DEPLOY_ENV} server..."
ansible-playbook -i "$INVENTORY_FILE" infrastructure/dump-database.yml -e "target_env=$DEPLOY_ENV"

# Find the most recent dump file
LATEST_DUMP=$(ls -t dumps/schmango_${DEPLOY_ENV}_*.sql 2>/dev/null | head -n1)

if [ -z "$LATEST_DUMP" ]; then
    echo ""
    echo "ERROR: No dump file found. Dump may have failed."
    exit 1
fi

echo ""
echo "→ Step 2: Restoring database to local development..."
ansible-playbook infrastructure/restore-database-local.yml -e "dump_file=$LATEST_DUMP"

echo ""
echo "========================================="
echo "✓ Database sync complete!"
echo "========================================="
echo ""
echo "Your local development database now matches ${DEPLOY_ENV}."
echo "You can now safely:"
echo "  • Make database model changes"
echo "  • Create migrations with: docker-compose run --rm web python manage.py makemigrations"
echo "  • Test locally with: docker-compose run --rm web python manage.py migrate"
