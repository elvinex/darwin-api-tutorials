# -*- coding: utf-8 -*-
"""
    DWX_API - Superclass for all sub-APIs
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: May 16, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

import os, requests
os.chdir('<INSERT-PATH-TO-PROJECT-DIR-HERE>')

from AUTH.dwx_oauth2_p3 import DWX_OAuth2
from MINIONS.dwx_file_io import load_config

class DWX_API(object):
    
    def __init__(self, 
                 _api_url='https://api.darwinex.com',
                 _api_name='darwininfo',
                 _version=1.4):
        
        # OAuth2 object for access/refresh token retrieval
        self._auth = DWX_OAuth2(load_config('CONFIG/creds_sample.cfg'))
        
        # Construct main production url for tagging endpoints
        self._url = '{}/{}/{}'.format(_api_url, _api_name, _version)
        
        # Construct authorization header for all requests
        self._auth_headers = {'Authorization': 'Bearer {}'.format(self._auth._data['access_token'])}
        
        # Construct headers for POST requests
        self._post_headers = {**self._auth_headers,
                              **{'Content-type':'application/json',
                                 'Accept':'application/json'}}
        
    ##########################################################################
    """
    Call any endpoint provided in the Darwinex API documentation, and get JSON.
    """
    def _Call_API_(self, _endpoint, _type, _data):
        
        # If 
        if _type not in ['GET','POST']:
            print('Bad request type')
            return None
        
        try:
            
            if _type == 'GET':
                _ret = requests.get(self._url + _endpoint,
                                    headers=self._auth_headers,
                                    verify=True)
                
            else:
                if len(_data) == 0:
                    print('Data is empty..')
                    return None
                
                _ret = requests.post(_endpoint,
                                     data=_data,
                                     headers = self._post_headers,
                                     verify=True)
        
            return _ret.json()
        
        except Exception as ex:
            print('Type: {0}, Args: {1!r}'.format(type(ex).__name__, ex.args))
            
    ##########################################################################