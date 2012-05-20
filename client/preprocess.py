'''function:create the file of myconfig to save user's information.'''
import wx

'''Before you run this application,please run this code first.'''
cfg = wx.Config('myconfig')
if cfg.Exists('ID'):
	cfg.Write('ID','')
	cfg.Write('PSW','')
	cfg.Write('state',False)
else:
	pass
