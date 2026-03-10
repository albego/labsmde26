#### Obtener en KQL el último evento de cada identificador

sensor_iot
| summarize arg_max(Timestamp, *) by ID_Sensor
