Content security policy (CSP)
-----------------------------
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