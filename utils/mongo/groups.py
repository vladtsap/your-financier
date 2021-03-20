from typing import List

from models.core import Group
from utils.mongo.core import MongoBase


class MongoGroups(MongoBase):

    def add(self, group: Group):
        self.groups.insert_one(group.to_dict())

    def is_new(self, member_id: int) -> bool:
        return not bool(list(self.groups.find(
            {'members': [member_id]}
        )))

    def get_by_member(self, member_id: int) -> List[Group]:
        return [
            Group.from_dict(group_content)
            for group_content in self.groups.find({"members": {"$in": [member_id]}})
        ]
