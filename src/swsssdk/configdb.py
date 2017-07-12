"""
SONiC ConfigDB connection module 

Example:
    config_db = ConfigDBConnector()
    config_db.connect()
    config_db.set_table('bgp_neighbor', '10.0.0.1', {
        'admin_status': state
        })

TODO:
    Will add API on keyspace subscription for incremental configuration support
    in the incoming versions.
"""

from .dbconnector import SonicV2Connector

class ConfigDBConnector(SonicV2Connector):

    def __init__(self):
        """Connect to Redis through TCP, which does not requires root.
        """
        super(ConfigDBConnector, self).__init__(host='127.0.0.1')

    def connect(self):
        SonicV2Connector.connect(self, self.CONFIG_DB, False)

    def set_table(self, table, key, data):
        """Write a table entry to config db.
        Args:
            table: Table name.
            key: Key of table row.
            data: Table row data in a form of dictionary {'column_key': 'value', ...}
        """
        client = self.redis_clients[self.CONFIG_DB]
        _hash = '{}:{}'.format(table.upper(), key)
        client.hmset(_hash, data)

    def get_table(self, table, key):
        """Read a table entry from config db.
        Args:
            table: Table name.
            key: Key of table row.
        Returns: 
            Table row data in a form of dictionary {'column_key': 'value', ...}
        """
        _hash = '{}:{}'.format(table.upper(), key)
        return SonicV2Connector.get_all(self, self.CONFIG_DB, _hash)

    def get_table_all(self, table):
        """Read an entire table from config db.
        Args:
            table: Table name.
        Returns: 
            Table data in a dictionary form of 
            { 'row_key': {'column_key': 'value', ...}, ...}
        """
        pattern = '{}:*'.format(table.upper())
        keys = SonicV2Connector.keys(self, self.CONFIG_DB, pattern)
        data = {}
        for key in keys:
            data[key.split(':')[1]] = SonicV2Connector.get_all(self, self.CONFIG_DB, key)
        return data

    def set_config(self, data):
        """Write multiple tables into config db. 
        Args:
            data: config data in a dictionary form
            { 
                'TABLE_NAME': { 'row_key': {'column_key': 'value', ...}, ...},
                ...
            }
        """
        for table_name, table_data in data.iteritems():
            for key, value in table_data.iteritems():
                self.set_table(table_name, key, value)

    def get_config(self):
        """Read all config data. 
        Returns:
            Config data in a dictionary form of 
            { 
                'TABLE_NAME': { 'row_key': {'column_key': 'value', ...}, ...},
                ...
            }
        """
        data = {}
        hashes = SonicV2Connector.keys(self, self.CONFIG_DB, '*')
        for _hash in hashes:
            table_name = _hash.split(':', 1)[0]
            key = _hash.split(':', 1)[1]
            if not data.has_key(table_name):
                data[table_name] = {}
            data[table_name][key] = SonicV2Connector.get_all(self, self.CONFIG_DB, _hash)
        return data

