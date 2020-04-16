#!/usr/bin/env python
# coding: utf-8

# Twitter: @xrths
# www.xrths.fr

# Importation des librairies.
from configparser import ConfigParser

config_folder = 'G:/COVID19-France/'


def get_config(section, option):
    config_parser = ConfigParser()
    config_parser.read(config_folder + 'config.ini')  # Modifier cette ligne.
    return config_parser.get(section, option)


def get_config_boolean(section, option):
    config_parser = ConfigParser()
    config_parser.read(config_folder + 'config.ini')  # Modifier cette ligne.
    return config_parser.getboolean(section, option)
