# Make Note

This command is a helper for creating new note files in the log.  It will create a new note file for the current date
and time based on the input template that is specified.

## Configuration

### Configuration File Details

This command can be configured using the configuration details stored in `config.yaml`.  The settings are stored under
the `make_note` key value.

```yaml
make_note:

  # The default template value to use when generating the log file.  This value can be overridden by a command line 
  # argument if necessary. 
  default_template: timeline_base
  
  # The editor that will be used to open the file after it has been created on the file system.  Use the string {file} 
  # for placing the path to the file.  
  editor: xdg-open {file}
```

### Command Line Arguments

This command is configured using command line arguments.

- `-t <template_name>` or `--template <template_name>`

  > Specify the template name that will be used to create the new log file.
  >
  > Default: timeline_base
  
- `-T` or `--template-list`

  > List all of the templates that are available to be used to generate a new log file.  Specifying this argument will
  > cause the command to exit after the list has been printed out.

## Example Execution

```bash
autology make_note -t project_base
```