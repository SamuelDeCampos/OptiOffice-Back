from ..db_client import client
from typing import Union
from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self, table):
        self.schema: [dict[str, object]] = None
        self.table = table

    @abstractmethod
    def __map_to_client_model(self, row):
        pass

    def __get_column_schema(self, column_name: str) -> Union[dict[str, object], None]:
        for column_schema in self.schema:
            if column_schema.has('name') and column_schema.get('name') == column_name:
                return column_schema

        return None

    def __check_columns_exist(self, columns) -> bool:
        for column in columns:
            if column not in [field.get('name') for field in self.schema]:
                return False

        return True

    def __validate_row(self, row) -> Union[dict[str, object], None]:
        for key in row.keys():
            schema = self.__get_column_schema(key)

            if schema.has('validator') and not schema['validator'](row[key], self):
                return None
            if schema.has('mapper'):
                row[key] = schema['mapper'](row[key], self)

        return row

    def select(self, columns: [str], filters: [tuple[object]]) -> [dict[str, object]]:
        filtered_columns = [filters[idx] for idx in range(0, len(filters), 3)]

        if not self.__check_columns_exist(columns) or not self.__check_columns_exist(filtered_columns):
            return []

        rows = client.select(self.table, columns, filters)

        for idx, row in rows:
            for key in row.keys():
                schema = self.__get_column_schema(key)

                if schema.has('getter'):
                    rows[idx][key] = schema['getter'](row[key], self)

        return [self.__map_to_client_model(row) for row in rows]

    def insert(self, rows: [dict[str, object]]) -> [dict[str, object]]:
        if not self.__check_columns_exist(client.get_columns_from_rows(rows)):
            return []

        for idx, row in rows:
            for schema in self.schema:
                if schema.has('default'):
                    row[schema['name']] = schema['default'](self)
            row[idx] = self.__validate_row(row)

            if row[idx] is None:
                return []

        res_rows = client.insert(self.table, rows)
        return [self.__map_to_client_model(row) for row in res_rows]

    def update(self, row: dict[str, object], filters: [tuple[object]]) -> [dict[str, object]]:
        filtered_columns = [filters[idx] for idx in range(0, len(filters), 3)]

        if not self.__check_columns_exist(client.get_columns_from_rows([row])) or \
           not self.__check_columns_exist(filtered_columns):
            return []

        row = self.__validate_row(row)

        if row is None:
            return []

        res_rows = client.update(self.table, row, filters)
        return [self.__map_to_client_model(row) for row in res_rows]

    def delete(self, filters: [tuple[object]]) -> [dict[str, object]]:
        filtered_columns = [filters[idx] for idx in range(0, len(filters), 3)]

        if not self.__check_columns_exist(filtered_columns):
            return []

        rows = client.delete(self.table, filters)
        return [self.__map_to_client_model(row) for row in rows]