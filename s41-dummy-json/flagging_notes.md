# Files
## all_assessment_ror_fund_round.json
JSON response for <assessment_store>/application_overviews/{fund_id}/{round_id}, with applications as below.

I've put full flag details for all flags inside each application as I thikn that'll be easier to retrieve from DB and lets us do the interpretation of what we display in the dashboard (multiple flags, flag stopped, whatever) in the frontend app. If we need to do this differently we could always reduce what comes back in application_overviews, but I think this gives us more flexibility for now.

## get_flags_for_application.json
JSON response for new endpoint <assessment_store>/{application_id}/flags GET, for application id ce946e9e-369e-472a-a9c3-c60cd124471b
I think we will need this endpoint rather than get_latest_flag as the 'flag history' show/hide thing is always present at the top of the application page so we will always want to retrieve all the flags, even tho we only display currently active ones in banners.

## get_avaialble_flag_allocations.json
JSON response for GET <fund_store>/{fund_id}/{round_id}/available_flag_allocations/
List the available flag allocations - keys and vlaues - for the create/update flag pages so we can list possible allocations. Can't have the enum values hardcoded anywhere as we need to be able to update these on the fly

## Still to do
Haven't yet done any json for create flag, update flag (ie resolve or stop).



# Application IDs
## ce946e9e-369e-472a-a9c3-c60cd124471b
Has multiple flags.
- b0ac84e5-bb97-4851-9ba3-4d1101030e9f
    - Currently raised, no further updates so still active

- f60f816e-0497-47a7-9211-1515f7939fbe
    - Previous flag, raised then resolved

## b8cb30b4-21b8-4255-ba33-6b53144964c4
No flags

## 4147f32f-580d-47a7-8a69-d0ebe4b6795d
No active flags, 2 resolved

## 0302354c-b478-4839-995b-6f9ebe0c0cd8
No active flags, one stopped

## 47f04631-cc36-44cd-95fa-8401bf55436c
One stopped flag, one other flag still unresolved

## 53762a02-e996-46e2-9ab4-d8ecfb91f3f9
One previously stopped flag, now resolved so not active


# Enum values

## flag.status values
- RAISED
- RESOLVED
- STOPPED

## flag.allocation and flag.update.allocation values
Ultimately will be provided by design and hard coded somewhere for now.
the allocation value is in multiple places at the moment to allow for what I think escalation will be, ie. changing the allocation.
so this way we have a 'current' allocation at the flag level, and history of where it was allocated at 'update' level.

Both key and value need to come from the database to allow for new teams to be added on the fly. See [get_avaialble_flag_allocations](./flagging_notes.md#get_avaialble_flag_allocationsjson)
