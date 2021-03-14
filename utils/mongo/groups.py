from typing import List

from models.core import Group
from utils.mongo import db

groups = db["groups"]


def is_registered(member_id: int) -> bool:
    return bool(list(groups.find({'members': [member_id]})))


def add_solo_group(group: Group):
    groups.insert_one(group.to_dict())


def get_groups_by_member(member_id: int) -> List[Group]:
    return [
        Group.from_dict(group_content)
        for group_content in groups.find({"members": {"$in": [member_id]}})
    ]
