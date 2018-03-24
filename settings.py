#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import warnings

'''
A module used to read and edit settings.

Example usage of new()(Depricated):

import settings as s
s.new('hello.cfg')
s.asetting = 'value'
if not s.exists('somesetting'):
    s.somesetting = 'something'
s.update()

Example usage of load():

import settings
s = settings.load('settingsfile.json')
s['setting'] = 'value'
s['alist'] = [1,2,3,4]
if not s.exists('somesetting'):
    s['somesetting'] = 'something'
s.close()
'''
class new:
    '''********************   Depricated   ********************
    Reads settings file and sets each setting as a attribute of self.'''
    def __init__(self, settingsfile, warn=True):
        warn = warnings.warn if warn else lambda *args, **kwargs: None
        warn("""settings.new() is depricated. Use settings.load() instead""",
        Warning)
        warn("Bad code ahead. Do not use settings.new()", SyntaxWarning)
        self.file = settingsfile
        self._settings ={}
        try:
            f = open(settingsfile,'r')
            data = f.readlines()
            f.close()
        except IOError:
            print('Settings File Not Found.')
            f = open(settingsfile, 'a')
            data = []
        for line in data:
            line = line.split(':')
            if line[0][0] == ' ':
                line[0] = line[1:]
            if len(line) == 1 and line[0] != '':
                name = line[0].strip()
                if name:
                	setattr(self, name, True)
                	self._settings[line[0]] = True
            elif len(line) == 1 and line[0] == '':
                pass
            elif len(line) == 2 and not line[0] == '':
                if line[1][0] == ' ':
                    line[1] = line[1][1:]
                value = line[1].replace('\n','')
                name = line[0].strip()
                if name:
                	setattr(self, name, eval(value))
                	self._settings[line[0]] = line[1].replace('\n','')
            elif len(line) == 2 and line[0] == '':
                pass
            else:
                raise SyntaxError('Invalid systax : ' +str(line))
    def update(self):
        '''********************   Depricated   ********************
        Update changed settings'''
        updater = []
        ignore = ['__doc__','__init__','__module__','_settings'
        ,'update','file','exists']
        for item in dir(self):
            if item not in ignore:
                value = getattr(self,item)
                if type(value) != str and type(value) != type:
                	updater.append(item+' : '+str(value))
                elif type(value) == str:
                	updater.append(item+' : '+'\'' + value + '\'')
                else:
                    updater.append(item+' : '+'\'' + str(value) + '\'')
        f = open(self.file,'w')
        for item in updater:
            f.write(item+'\n')
        f.close()
    def exists(self,var):
        '''********************   Depricated   ********************
        Check if setting exists'''
    	return hasattr(self,var)
class settingsdict(dict):
    '''A subclass of Dict with additional methods.'''
    def path(self):
        '''Get path to the settings file'''
        return self.settingspath

    def sync(self):
        '''Update settings file with current values'''
        open(self.settingspath, 'w').close()
        f = open(self.settingspath,'w')
        data = eval(self.__repr__())
        json.dump(data, f,indent=1,sort_keys=True)

    def close(self):
        '''Update settings file with current values and clear Dict'''
        self.sync()
        self.clear()
    def __enter__(self):
        '''Adds support for use with the 'with' statement'''
        return self
    def __exit__(self,exc_type, exc_value, traceback):
        '''Adds support for use with the 'with' statement'''
        self.sync()
    def exists(self,value):
        '''Check if setting exists'''
        return self.__contains__(value)
    settingspath = None
def load(filename):
    '''Opens a json settings file and create a settingsdict instance from it.
        Creates empty file if file does not exist'''
    if filename.startswith('~/'):
        filename = os.path.join(os.path.expanduser("~"),'.config',filename[2:])
    try:
        f = open(filename,'r')
    except IOError:
         f = open(filename,'a')
         f.write('{}')
         f.close()
         f = open(filename,'r')
    try:
        data = json.load(f)
    except ValueError:
        data = json.loads('{}')
    settings = settingsdict(data)
    settings.settingspath = filename
    return settings
