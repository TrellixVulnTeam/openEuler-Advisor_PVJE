#!/usr/bin/python3
"""
    Description:Read the base class of the configuration file in the system
                which mainly includes obtaining specific node values
                and obtaining arbitrary node values
    Class:ReadConfig
"""
import configparser
from configparser import NoSectionError
from configparser import NoOptionError
from packageship.system_config import SYS_CONFIG_PATH


class ReadConfig():
    """
    Description: Read the configuration file base class in the system
    Attributes:
        conf:Configuration file for the system
        conf.read:Read the system configuration file
    """

    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read(SYS_CONFIG_PATH)

    def get_system(self, param):
        """
        Description: Get any data value under the system configuration node
        Args:
            param:The node parameters that need to be obtained
        Returns:
        Raises:
        """
        if param:
            try:
                return self.conf.get("SYSTEM", param)
            except NoSectionError:
                return None
            except NoOptionError:
                return None
        return None

    def get_database(self, param):
        """
        Description: Get any data value under the database configuration node
        Args:
            param:The node parameters that need to be obtained
        Returns:
        Raises:
        """
        if param:
            try:
                return self.conf.get("DATABASE", param)
            except NoSectionError:
                return None
            except NoOptionError:
                return None
        return None

    def get_config(self, node, param):
        """
        Description: Get configuration data under any node
        Args:
            node:node
            param:The node parameters that need to be obtained
        Returns:
        Raises:
        """
        if all([node, param]):
            try:
                return self.conf.get(node, param)
            except NoSectionError:
                return None
            except NoOptionError:
                return None
        return None