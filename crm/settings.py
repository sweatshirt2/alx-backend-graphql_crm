CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]

INSTALLED_APPS = [
    'django_crontab',
]

CRONJOBS = [
    # other cron jobs...
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]
