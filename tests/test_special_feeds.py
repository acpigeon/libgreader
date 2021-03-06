#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
libG(oogle)Reader
Copyright (C) 2010  Matt Behrens <askedrelic@gmail.com> http://asktherelic.com

Python library for working with the unofficial Google Reader API.

Unit tests for feeds. Requires mechanize for automated oauth authenication.

"""

try:
    import unittest2 as unittest
except:
    import unittest

from libgreader import GoogleReader, OAuthMethod, ClientAuthMethod, Feed, ItemsContainer, Item, BaseFeed, SpecialFeed, ReaderUrl
import urllib
import urllib2
import urlparse
import mechanize
import re
import time

from config import *

class TestSpecialFeeds(unittest.TestCase):
    def test_reading_list_exists(self):
        ca = ClientAuthMethod(username,password)
        reader = GoogleReader(ca)
        reader.makeSpecialFeeds()
        feeds = reader.getFeedContent(reader.getSpecialFeed(ReaderUrl.READING_LIST))

        self.assertEqual(dict, type(feeds))

        list_match = re.search('reading list in Google Reader', feeds['title'])
        self.assertTrue(list_match)

    def test_marking_read(self):
        ca = ClientAuthMethod(username,password)
        reader = GoogleReader(ca)
        container = SpecialFeed(reader, ReaderUrl.READING_LIST)
        container.loadItems()

        feed_item = container.items[0]
        self.assertTrue(feed_item.markRead())
        self.assertTrue(feed_item.isRead())

    def test_loading_item_count(self):
        ca = ClientAuthMethod(username,password)
        reader = GoogleReader(ca)
        container = SpecialFeed(reader, ReaderUrl.READING_LIST)
        container.loadItems(loadLimit=5)

        self.assertEqual(5, len(container.items))
        self.assertEqual(5, container.countItems())

    def test_subscribe_unsubscribe(self):
        ca = ClientAuthMethod(username,password)
        reader = GoogleReader(ca)
        
        slashdot = 'feed/http://rss.slashdot.org/Slashdot/slashdot'

        #unsubscribe always return true; revert feedlist state
        self.assertTrue(reader.unsubscribe(slashdot))

        # now subscribe
        self.assertTrue(reader.subscribe(slashdot))

        # wait for server to update
        time.sleep(1)
        reader.buildSubscriptionList()

        # test subscribe successful
        self.assertIn(slashdot, [x.id for x in reader.getSubscriptionList()])

if __name__ == '__main__':
    unittest.main()
