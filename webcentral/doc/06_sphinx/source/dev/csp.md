# Content security policy (CSP)
The CSP is a security feature that helps prevent cross-site scripting (XSS), clickjacking, and other code injection attacks resulting from execution of malicious content in the trusted web page context.
One way to implement CSP is to add a Content-Security-Policy HTTP header to your web server responses. The header value is a string that defines the policy. The policy is a set of directives that specify the content sources that the browser should consider acceptable for the web page. The browser will only execute or render resources from those sources.
For example, the following CSP header specifies that the browser should only load resources from the same origin as the web page, and should not execute inline scripts or styles.
When the browser receives this header, it will enforce the policy by blocking any resources that do not comply with the specified directives.
When ressources from other origins are needed, the links to these ressources have to be mentioned explicitly.
For Django, a package called django-csp is available to help you implement CSP in your Django project. To add a link, which is considered as a trusted source, it has to be added to the `01_application/webcentral_app/webcentral_app/settings.py` file in the `CSP_SCRIPT_SRC` and `CSP_STYLE_SRC` lists.
The following code shows trusted sources for scripts and styles:
```
CSP_SCRIPT_SRC = (
    "'self'",
    "https://ajax.googleapis.com",
    "https://cdnjs.cloudflare.com",
    "https://maxcdn.bootstrapcdn.com",
    "https://cdn.plot.ly",
    "https://unpkg.com",
    "https://code.highcharts.com/highcharts.js",
    "https://cdn.jsdelivr.net/gh/harvesthq/chosen@1.8.7/chosen.jquery.min.js",
)

CSP_STYLE_SRC = (
    "'self'",
    "https://maxcdn.bootstrapcdn.com",
    "https://cdnjs.cloudflare.com",
    "https://cdn.plot.ly",
    "https://unpkg.com",
    "https://cdn.jsdelivr.net/gh/harvesthq/chosen@1.8.7/chosen.min.css",
)
```

## Solving browser caching issues
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
