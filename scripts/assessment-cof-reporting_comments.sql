SELECT
	application_id,
	short_id,
	jsonb_path_query_first (jsonb_blob, '$.forms[*].questions[*].fields[*] ? (@.key == "WWWWxy")."answer"') AS "Unique Tracker Number",
	jsonb_path_query_first (jsonb_blob, '$.forms[*].questions[*].fields[*] ? (@.key == "YdtlQZ")."answer"') AS "Organisation Name",
	jsonb_path_query_first (jsonb_blob, '$.forms[*].questions[*].fields[*] ? (@.key == "lajFtB")."answer"') AS "Organisation Type",
	jsonb_path_query_first (jsonb_blob, '$.forms[*].questions[*].fields[*] ? (@.key == "KAgrBz")."answer"') AS "Project Name",
	jsonb_path_query_first (jsonb_blob, '$.forms[*].questions[*].fields[*] ? (@.key == "LZBrEj")."answer"') AS "Lead Contact Email Address",
	funding_amount_requested AS "Funding Amount Requested",
	jsonb_path_query_first (jsonb_blob, '$.forms[*].questions[*].fields[*] ? (@.key == "NdFwgy")."answer"') AS "Capital Costs",
	jsonb_path_query_first (jsonb_blob, '$.forms[*].questions[*].fields[*] ? (@.key == "NyudvF")."answer"') AS "Revenue Costs",
	asset_type AS "Asset Type",
	jsonb_path_query_first (jsonb_blob, '$.forms[*].questions[*].fields[*] ? (@.key == "GjzaqR")."answer"') AS "Asset Type Other",

	jsonb_path_query_first (jsonb_blob, '$.forms[*].questions[*].fields[*] ? (@.key == "yEmHpp")."answer"') AS "Address",

	location_json_blob -> 'postcode' AS "Postcode",
	location_json_blob -> 'county' AS "County",
	location_json_blob -> 'country' AS "Country",
	location_json_blob -> 'constituency' AS "Constituency"

FROM assessment_records

WHERE "workflow_status" = 'COMPLETED'