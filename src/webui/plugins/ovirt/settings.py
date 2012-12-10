'''
Created on Nov 15, 2012

@author: mmornati
'''
STORAGE_TYPES = (
    ('', '-- Select --'),
    ('system', 'System'),
    ('data', 'Data'),
    ('iso', 'ISO'),
    ('export', 'Export'),
)

STORAGE_INTERFACE = (
    ('', '-- Select --'),
    ('virtio', 'VirtIO'),
    ('ide', 'IDE'),
    ('scsi', 'SCSI'),
)

STORAGE_FORMAT = (
    ('', '-- Select --'),
    ('cow', 'Cow'),
    ('raw', 'Raw'),
)

NETWORK_INTERFACE_TYPE = (
    ('', '-- Select --'),
    ('virtio', 'VirtIO'),
    ('e1000', 'e1000'),
    ('rtl8139', 'rtl8139'),
)