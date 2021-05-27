from supabase_py import Client
from supabase_py.client import SupabaseQueryBuilder
from ..setup.db import dbClient


class Model:
    def __init__(self, columns: dict[str, object], table: str):
        self.__client: Client = dbClient
        self.__columns = columns
        self.__table = self.__client.table(table)

    def __rowsCheck(self, row: dict[str, object]):
        for key, value in row:
            if key not in self.__columns:
                raise Exception("Key doesn't exist")
            if type(value) is not type(self.__columns[key]):
                raise Exception("Wrong type")

    def __create(self, rows: [dict[str, object]]):
        for row in rows:
            self.__rowsCheck(row)
            self.__table.insert(row)\
                .execute()

    def __read(self, columns: str, filters: str, foreignTable: str) -> SupabaseQueryBuilder:
        return self.__table.select(columns)\
            .execute()

    def __update(self, filters: str, foreignTable: str, row: dict[str, object]):
        self.__rowsCheck(row)
        self.__table\
            .update(row)\
            .execute()

    def __delete(self, filters: str):
        self.__table\
            .delete()\
            .execute()