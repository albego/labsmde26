sensor_iot
| summarize arg_max(Timestamp, *) by ID_Sensor
