__author__="jwong"
__date__ ="$Aug 16, 2009 6:32:20 PM$"

class ViewBase:
    def __init__(self, view):
        self.view = view
        self.controller = view.controller
