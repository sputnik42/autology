# Timeline Plugin

This is a plugin that will process all of the markdown files that are provided to it and build a 
collection of reports organized by date and time.

## Configuration

N/A 

## Log Inputs

### Markdown Front Matter Content

The timeline plugin only looks at one value stored in the front matter.

- `time`
  
  > The time value for when the post should be listed in the log definition.  This value can be provided in the 
  > following formats.
  >
  > HH:MM:SS
  > YYY-mm-dd HH:MM:SS.mmmmm

## Generated Reports

### Main Report

Contains a list of all the dates that have logs associated with them.

#### Template Path Definition

- timeline
    - index

#### Publishing Context

- `dates` 
 
  > List of DayReports that contain the following data
  
  - `date` 
   
     > python date object containing the date log
     
  - `url`
  
     > URL for the report containing the entries for that date
     
  - `num_entries`
    
     > Number of entries associated with that day's reports
     
  - `max_year` 
  
     > Highest year value for all of the logs recorded
     
  - `min_year`
  
     > Lowest year value for all of the logs recorded

### Daily Report 

Contains the contents of the logs concatenated together into a large HTML file.

#### Template Path Definition

- timeline
    - day

#### Publishing Context

- `entries`

  > List of lists containing the date and the front matter post. 
