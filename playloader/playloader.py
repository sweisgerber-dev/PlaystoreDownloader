#!/usr/bin/env python
# coding: utf-8

import argparse
import datetime
import json
import logging as log
import os
import sys

from ..util.logutil import Logger
from ..util.stringutils import StringUtils
from ..config.apkconfig import ApkConfig
from ..config.playloaderconfig import PlayLoaderConfig

from ..playstore.playstore import Playstore

class PlayLoader:

    def __init__(self, credentials:str=PlayLoaderConfig.credentials_default_location) -> None:
        super().__init__()
        Logger.setup_logging()
        self.api = Playstore(credentials)

    def download(self, package_name: str, download_folder: str = PlayLoaderConfig.downloaded_apk_default_location, binary_blobs=False, infos_json=True, infos_proto=False):

        # Make sure to use a valid json file with the credentials.

        if not os.path.exists(download_folder):
            log.info('~ Path: {} does not exist'.format(download_folder))
            return None

        try:
            # Get the application details.
            app = self.api.app_details(package_name).docV2
            app_details = self.api.protobuf_to_dict(app)
            # log.infoapp_details_dict)
            # json.dumps(app)
            # log.infoapp)
        except AttributeError:
            log.info('Error when downloading "{0}". Unable to get app\'s details.'.format(package_name))
            return None

        details = {
            'package_name': app.docid,
            'title': app.title,
            'creator': app.creator,
            'download_date': datetime.datetime.today().strftime('%Y-%m-%d')
        }
        try:
            details['version'] = app_details['details']['appDetails']['file'][0]['versionCode']
        except KeyError:
            details['version'] = 0

        log.info(details)

        # The downloaded apk will be saved in the Downloads folder (created in the same folder as this script).
        downloaded_apk_file_path = os.path.join(
            download_folder,
            ApkConfig.APK_FILENAME.format(
                details['package_name'],
                details['version'],
                details['download_date']
            ))
        downloaded_info_file_path = StringUtils.rreplace(downloaded_apk_file_path, '.apk', '.proto', 1)
        downloaded_json_file_path = StringUtils.rreplace(downloaded_apk_file_path, '.apk', '.json', 1)

        # If it doesn't exist, create the directory where to save the downloaded apk.
        # if not os.path.exists(os.path.dirname(downloaded_apk_file_path)):
        #     os.makedirs(os.path.dirname(downloaded_apk_file_path))


        # The download of the additional .obb files is optional.
        if binary_blobs:
            success = self.api.download(details['package_name'], downloaded_apk_file_path, download_obb=True)
        else:
            success = self.api.download(details['package_name'], downloaded_apk_file_path, download_obb=False)

        if not success:
            log.info('Error when downloading "{0}".'.format(details['package_name']))
            return None
        else:
            if infos_proto:
                with open(downloaded_info_file_path, 'w') as protobuf_file:
                    protobuf_file.write(str(app))
            if infos_json:
                with open(downloaded_json_file_path, 'w') as json_file:
                    json.dump(app_details, json_file, indent=2)
