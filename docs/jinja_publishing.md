# Jinja2 Publishing Plugin

The default publishing functionality is provided by Jinja2. 

## Configuration Details

All of the configuration details for jinja are placed in the `publishing` section of `config.yaml`.

```yaml
# JINJA2 Configuration details
publishing:
  # Location where all of the output files will be placed after rendering content
  output: output
  
  # Location where the jinja templates are located on the file system.
  templates: templates
  
  # URL prefix that will be used inside templates.  This is useful in case the output of the 
  # application is not located in the root of the webserver.
  url_root: ''
```
