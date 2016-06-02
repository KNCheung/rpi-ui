from .DataSourceBase import Timer

dataSources = {}

from .DateTime import DateTime
dataSources['DateTime'] = DateTime

from .AM2302 import AM2302
dataSources['AM2302'] = AM2302

from .CPUUsage import CPUUsage
dataSources['CPUUsage'] = CPUUsage

from .CPUTemp import CPUTemp
dataSources['CPUTemp'] = CPUTemp

from .Wlan0_IP import Wlan0_IP
dataSources['Wlan0_IP'] = Wlan0_IP

from .Elec import Elec
dataSources['Elec'] = Elec

from .CdSSensor import CdSSensor
dataSources['CdSSensor'] = CdSSensor

