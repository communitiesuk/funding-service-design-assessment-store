# 📜 Scripts

## Import from application.

To import all the application jsons from the application store for a specific `round_id` you run (from project root):
`python -m scripts.import_from_application --roundid={your round id}`

## Process Locations

Use the functions in this script to extract postcodes from form data, request the location details from postcodes.io and process this into json we can use in the application.

It expects raw form data in the file specified at the top of the script (`file_raw_forms_data`). To obtain this data you need to login via cloudfoundry with conduit installed and execute:

    cf conduit <db_service_name> -c '{"read_only": true}' -- psql -c "select json from forms where name ='project-information';" > dev_forms_raw.txt
