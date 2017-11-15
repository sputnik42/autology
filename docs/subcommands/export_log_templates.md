# Export Log Templates

Dump all of the log generation templates to a directory.  These files can then be used for the generation of content 
when not using the `make_note` command (i.e. when on a phone).

## Configuration

This command is configured through command line arguments.

- `-o <dir_name>` or `--output-dir <dir_name>`

  > Specify the output directory of the template files
  >
  > Default: templates/generation
  
## Example Execution

```bash
autology export_log_templates -o templates/logs
```
