#!/bin/bash

# Log file location
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Get current timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Execute Django shell command to delete inactive customers and count them
DELETED_COUNT=$(python3 manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True, created_at__lt=one_year_ago).distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Append log with timestamp and count
echo \"$TIMESTAMP - Deleted $DELETED_COUNT inactive customers\" >> \"$LOG_FILE\"
# "${BASH_SOURCE[0]}", "pwd", "cwd", "cd", "if", "else"
