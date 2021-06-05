import requests
from urllib.parse import urlencode
import json

from config import DB_CONFIG


class RequestFiltersException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class DatabaseClient:
    def __init__(self, dbId: str, dbKey: str):
        self.__url = f'https://{dbId}.supabase.co/rest/v1/'
        self.__header = {
            'accept': '*/*',
            'accept-Encoding': 'gzip, deflate',
            'apikey': str(dbKey),
            'authorization': f'Bearer {dbKey}',
            'connection': 'close',
            'content-profile': 'public',
            'content-Type': 'application/json',
            'host': f'{dbId}.supabase.co',
            'prefer': 'return=representation'
        }

        self.__filters_operators = {
            'eq': 'eq',
            'neq': 'neq',
            'gt': 'gt',
            'gte': 'gte',
            'lt': 'lt',
            'lte': 'lte',
            'like': 'like',
            'ilike': 'ilike',
            'is': 'is',
            'in': 'in',
            'cs': 'cs',
            'cd': 'cd',
            'sl': 'sl',
            'sr': 'sr',
            'nxl': 'nxl',
            'nxr': 'nxr',
            'adj': 'adj',
            'ov': 'ov',
            'fts': 'fts',
            'plfts': 'plfts',
            'phfts': 'phfts',
            'wfts': 'wfts'
        }

    def __readFilters(self, filters: [tuple[object]]) -> dict[str, object]:
        url_params = {}

        for f in filters:
            words_len = len(f)
            param_value = ''

            if words_len % 3 != 0:
                raise RequestFiltersException('Wrong filters format')

            for idx in range(1, len(f), 3):
                if f[idx] not in self.__filters_operators:
                    raise RequestFiltersException(f'Filter operator {f[idx]} does not exist')

            if words_len == 3:
                url_params.update({f[0]: f'{f[1]}.{f[2]}'})
                continue

            for idx in range(0, len(f), 3):
                or_filter = f'{f[idx]}.{f[idx + 1]}.{f[idx + 2]}'
                param_value = f'{param_value},{or_filter}' if param_value != '' else or_filter
            url_params.update({'or': f'({param_value})'})

        return url_params

    def select(self, table: str, columns: [str], filters: [tuple[object]]) -> dict[str, object]:
        url = f'{self.__url}{table}'
        params = {'select': ','.join(columns)}
        params.update(self.__readFilters(filters))

        return json.loads(requests.get(url, headers=self.__header, params=params).text)

    def insert(self, table: str, rows: [dict[str, object]]) -> dict[str, object]:
        columns = rows[0].keys()

        for row in rows:
            missing = list(set(columns) ^ set(row.keys()))

            if len(missing) > 0:
                columns.append(missing[0])

        params = {'columns': ','.join(columns)}
        url = f'{self.__url}{table}?{urlencode(params)}'

        return json.loads(requests.post(url, headers=self.__header, data=json.dumps(rows)).text)

    def update(self, table: str, row: dict[str, object], filters: [tuple[object]]) -> dict[str, object]:
        url = f'{self.__url}{table}'
        params = self.__readFilters(filters)

        return json.loads(requests.patch(url, headers=self.__header, params=params, data=json.dumps(row)).text)

    def delete(self, table: str, filters: [tuple[object]]) -> dict[str, object]:
        url = f'{self.__url}{table}'
        params = self.__readFilters(filters)

        return json.loads(requests.delete(url, headers=self.__header, params=params).text)


client = DatabaseClient(DB_CONFIG.get('HOST_URL'), DB_CONFIG.get('HOST_KEY'))
