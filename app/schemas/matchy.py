
from pydantic import BaseModel
from app.enums import ConditonProperty, Comparer, FieldType
from typing import List, Dict


class MyBaseModel(BaseModel):
    class config:
        orm_mode = True


class MatchyCondition(MyBaseModel):
    property: ConditonProperty
    comparer: Comparer | None = None
    value: int | str | List[str]
    custom_fail_message: str | None = None


class MatchyOption(MyBaseModel):
    display_value: str
    value: str | None = None
    mandatory: bool | None = False
    type: FieldType
    conditions: List[MatchyCondition] | None = []


class ImportPossibleFields(MyBaseModel):
    possible_fields: List[MatchyOption] = []

class MatchyCell(MyBaseModel):
    value: str
    rowIndex: int
    colIndex: int

# employees to be added to the db after front validation
class MatchyUploadEntry(MyBaseModel):
    lines: List[Dict[str, MatchyCell]] # [{"fname":{"Rahim",0,0}}, {}]
    force_upload: bool = False


# MatchyUploadEntry looks like this:
# {
#     "lines":
#         [
#             {
#                 "first_name":{
#                     "value":"Rahim",
#                     "rowIndex":0,
#                     "colIndex":0
#                 }
#             },
#             {
#                 "first_name":{
#                     "value":"Rahim",
#                     "rowIndex":0,
#                     "colIndex":0
#                 }
#             }
#         ]
# }
