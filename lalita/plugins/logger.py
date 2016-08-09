# -*- coding: utf8 -*-

import os
import logging
import logging.handlers

from lalita import Plugin


class Logger(Plugin):
    '''Log channel to a directory'''

    def init(self, config):
        self.logger.info("Logger config: %s", config)

        self.base_dir = config.get('base_dir')
        if not self.base_dir:
            raise RuntimeError('Base dir not provided for logger plugin')
        self.loggers = {}

        self.register(self.events.PUBLIC_MESSAGE, self.log_public_message)
        
    def get_logger_for_channel(self, channel):
        """Configure a logger for the given channel"""
        
        # Get the logger and return it if it exists
        logger = self.loggers.get(channel)
        if logger:
            return logger
        
        # Build a logger
        logger = logging.getLogger('lalita_logger_' + channel)
        logger.setLevel(logging.INFO)
        path = os.path.join(self.base_dir, channel + '.log')
        
        # Setup handler and formatter
        handler = logging.handlers.TimedRotatingFileHandler(
            path,
            when='D',
            interval=1,
            backupCount=0,
            encoding='utf-8',
        )
        formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Add logger to the cache
        self.loggers[channel] = logger

        return logger

    def log_public_message(self, user, channel, message):
        logger = self.get_logger_for_channel(channel)
        logger.info('[%s] %s', user, message)
