# Running the app in production
The following sections address topics, which come up when running the Application in production.

## Cache busting techniques
When developing the application in an agile manner lots of changes will be introduced to the web application when its already running publicly. Because of that problems can arise. One problem has to do with the client browser caches static files (javascript/stylesheet-files) to reduce loading time. This can lead to websites look broken for clients re-visiting the website since the still use the old cached versions. 
To address that problem a static files bundler `webpack` is used. It transpiles the `scss`-files into one `css`-file. A hash-value is also put into the filename. The also installed package `wepback-bundler-tracker` creates a file `weback-stats.json` where the location of the created css-files is stored. The stats file is then used by the package `django-weback-loader` to insert the most up-to-date file in stylesheet link tag in the django templates.

The configuration of `django-weback-loader` is done in the `settings.py`-file. There, the following lines were added:
```python
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '/webpack_bundles/',
        'CACHE': not DEBUG,
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
    }
}
```
The location of the transpiled bundles are specified in the `BUNDLE_DIR_NAME` constant. The location specified must be reachable from within the location specified in the `STATICFILES_DIR` constant.
The location of the `webpack-bundler-loader` stats-file is specfied in `STATS_FILE`. A absolute path is taken as input. Furthermore the intervall in which changes in the stats file are checked can be set via `POLL_INTERVAL` in seconds. Polling is only activated if the django `DEBUG`-flag is set to true. `DEBUG` beeing `True` typically means that django is executed in a development environment, and `DEBUG` equals `False` is set on a production instance.  



