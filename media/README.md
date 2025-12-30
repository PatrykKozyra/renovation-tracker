# Media Files - DEPRECATED

**⚠️ This directory is no longer used.**

All media files are now stored on the D: drive at:
`D:\renovation-tracker-media\`

This change was made to save space on the C: drive.

## Configuration
See `config/settings/base.py`:
```python
MEDIA_ROOT = Path('D:/renovation-tracker-media')
```

Do not store files here - they will not be accessible by the application.
