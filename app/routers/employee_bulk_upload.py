
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.dependencies import DbDep
from app import schemas, utils

router = APIRouter(
    tags=["Bulk Upload Employees"]
)


@router.get("/possible_fields")
def get_possible_import_fields(session: DbDep):
    return schemas.ImportPossibleFields(possible_fields=utils.options)


@router.post("/employees_bulk_upload")
async def employees_validation_and_bulk_upload(
    entry: schemas.MatchyUploadEntry,
    background_tasks:BackgroundTasks,
    session: DbDep
):
    employees = entry.lines
    force_upload = entry.force_upload
    # a whole column is missing (so we can verify employees[0] only)
    missing_mandatory_fields = list(set(utils.mandatory_fields.keys()) - set(employees[0].keys()))

    if missing_mandatory_fields:
        missing_fields_names = [utils.mandatory_fields[val] for val in missing_mandatory_fields]
        raise HTTPException(
            status_code=400,
            detail=f"missing mandatory fields: { ', '.join(missing_fields_names) }"
        )

    return utils.validate_employees_data_and_upload(
        employees=employees,
        background_tasks= background_tasks,
        force_upload=entry.force_upload,
        db=session
    )
