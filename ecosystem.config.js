module.exports = {
  apps: [
    {
      name: 'manglam-furniture',
      cwd: '/home/ubuntu/chetanshop',
      script: 'gunicorn',
      args: 'manglam_furniture.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120',
      interpreter: '/home/ubuntu/chetanshop/.venv/bin/python',
      exec_mode: 'fork',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        DJANGO_SETTINGS_MODULE: 'manglam_furniture.settings.production',
        PORT: '8000'
      }
    }
  ]
};
