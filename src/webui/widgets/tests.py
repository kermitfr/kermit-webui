from webui.widgets.base import Widget

import unittest

class BasicCalendarTestCase(unittest.TestCase):
    def test_templatetag(self):
        
        class TestWidget(Widget):
            template = "hello.html"
            
            def get_context(self):
                return {"hello":"world"}
