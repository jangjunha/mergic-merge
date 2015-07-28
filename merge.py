# -*- coding: utf-8 -*-
from pydub import AudioSegment
from StringIO import StringIO
import urllib
import requests
import logging
import mergic_merge_config as config


def do_merge(music_id, plays):
    # Download plays
    local_plays = []
    for play in plays:
        sp = play.rsplit('/', 1)
        play_name = sp[1]
        local_name = "tmp/%s--%s" % (music_id, play_name)
        urllib.urlretrieve(play, local_name)
        local_plays.append(local_name)

    # Merge plays
    sound = AudioSegment.from_mp3(local_plays[0])
    print "S0: %s" % local_plays[0]
    for i in xrange(1, len(local_plays)):
        snow = AudioSegment.from_mp3(local_plays[i])
        sound = sound.overlay(snow, position=0)

        print "S%d: %s" % (i, local_plays[i])

    exported_filename = "tmp/%s.mp3" % music_id
    exported_music = sound.export(exported_filename, "mp3")

    url = '/'.join([config.MERGIC_GAE_URL, 'conn', 'update_music'])
    data = {'SECRET_KEY': config.MERGESVR_SECRET_KEY,
            'music_id': music_id}
    files = {'file': exported_music}
    r = requests.post(url, data=data, files=files)

    # Make FileItem
    # url = '/'.join([app.config['MERGIC_GAE_URL'],
    #'conn', 'mk_fileitem_music'])
    # data = {'SECRET_KEY': app.config['MERGESVR_SECRET_KEY'],
    #         'music_id': music_id}
    # r = requests.post(url, data=data)
    # j = r.json()
    # file_id = j['file_id']
    # file_name = "%s.mp3" % file_id
    # item_name = '/'.join(['mergic_music', file_name])

    # Send merged music to CloudStorage
    # with gcs.open(item_name,
    #               'w', content_type="audio/mp3",
    #               options={'x-goog-acl': 'public-read'}) as f:
    #     f.write(exported_music.read())

    # Set Music.music_file to fileitem.id
    # url = '/'.join([app.config['MERGIC_GAE_URL'],
    #                 'conn',
    #                 'set_music_fileitem'])
    # data = {'SECRET_KEY': app.config['MERGESVR_SECRET_KEY'],
    #         'file_id': file_id,
    #         'music_id': music_id}
    # r = requests.post(url, data=data)

    print "Task finished: %s" % exported_filename
