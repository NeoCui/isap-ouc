#!/usr/bin/python
# -*- coding: utf-8 -*-
'''this file is to save user's choice and set user's choice.'''

respond = [False, False, False]

def SetOne(s1,s2,s3):
	global respond
	respond = [s1, s2, s3]

def SetTwo():
	global respond
	return respond
