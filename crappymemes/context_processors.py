#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def giphy_processor(request):
    gifs = []
    try:
        r = requests.get("http://api.giphy.com/v1/gifs/trending?api_key=dc6zaTOxFJmzC").json()
        gif_candidates = [obj for obj in r['data'] if (obj['embed_url'])]
        for gif in gif_candidates:
            gifs.append(gif['embed_url'])
    except (IOError, KeyError):
        pass
    return {'gifs': gifs[:12]}



