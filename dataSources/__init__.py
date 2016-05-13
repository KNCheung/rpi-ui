from .DataSourceBase import Timer

dataSources = {}

from .DateTime import DateTime
dataSources['DateTime'] = DateTime

from .AM2302 import AM2302
dataSources['AM2302'] = AM2302

