#! /usr/bin/env python
# encoding: utf-8

"""
rhythmstring.py

Get a rhythm string from The Echo Nest API for any Spotify track URI.

Created by Tristan Jehan on 2013-08-12.
Modified by jmarmor@gmail.com on 2015-06-20.
Copyright (c) 2013 The Echo Nest. All rights reserved.

The rhythmstring format goes as follows:
Fs Hop Nch <Nos Oi do_1 ... do_n> ... <Nos Oi do_1 ... do_n>

where:
Fs: sampling rate
Hop: hop size
Nch: number of echoprint channels
Cm: channel index
Nos: number of onsets
Oi: intial onset frame
do_n: number of frames to the next onset

"""

import os
import zlib
import base64
import json
import sys

import numpy as np
import requests
import pyen


en = pyen.Pyen(os.environ["ECHONEST_API_KEY"])
#en = pyen.Pyen()

def get_by_spotify_track_artist(artist):
    return get_song_onsets(
        'song/search',
        {
            #'track_id': spotify_track_uri
            'artist' : artist
        }
    )

def get_by_spotify_track_song(title,artist):
    return get_song_onsets(
        'song/search',
        {
            #'track_id': spotify_track_uri
            'title' : title,
            'artist' : artist
        }
    )


def get_song_onsets(method, params):
    """
    examples:
        get_song_onsets(
            'song/profile',
            {'track_id': 'spotify:track:7uYvKcX4hJ4YUVV06qsmer'}
        )
        get_song('song/search', {'artist': 'jonathan marmor'})

    """

    params.update({
        'results': 1,
        'bucket': 'audio_summary',
    })
    song = en.get(method, **params)

    analysis_url = song['songs'][0]['audio_summary']['analysis_url']
    analysis = requests.get(analysis_url).json()

    rhythmstring = analysis['track']['rhythmstring']

    onsets = get_onsets(rhythmstring)

    return onsets


def decode_string(s):
    if s == None or s == '':
       return None
    l = [int(i) for i in s.split(' ')]
    Fs = l.pop(0)
    Hop = l.pop(0)
    frame_duration = float(Hop) / float(Fs)
    Nch = l.pop(0)
    onsets = []
    n = 0
    for i in range(Nch):
        N = l[n]
        n += 1
        for j in range(N):
            if j == 0:
                ons = [l[n]]
            else:
                ons.append(ons[j - 1] + l[n])
            n += 1
        onsets.append(ons)
    new_onsets = []
    for ons in onsets:
        new_ons = []
        for o in ons:
            new_ons.append(o * frame_duration)
        new_onsets.append(new_ons)
    return new_onsets


def decompress_string(compressed_string):
    compressed_string = compressed_string.encode('utf8')
    if compressed_string == '':
        return None
    try:
        actual_string = zlib.decompress(
            base64.urlsafe_b64decode(compressed_string)
        )
    except (zlib.error, TypeError):
        print 'Could not decode base64 zlib string {}'.format(compressed_string)
        return None
    return actual_string


def get_onsets(rhythmstring):
    decompressed_string = decompress_string(rhythmstring)
    return decode_string(decompressed_string)

def getOnsets(artist,song):
    if song != '':
        onsets = get_by_spotify_track_song(song,artist)
    else:
        onsets = get_by_spotify_track_artist(artist)
    return onsets
