CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]

INSTALLED_APPS = [
    'django_crontab',
]
