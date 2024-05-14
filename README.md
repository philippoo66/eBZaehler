# eBZaehler
listen to eBZ DD3 OD electricity meter (port on top) and publish MQTT 

The port on top delivers extensive info like this every single second:

`EBZ5DD32R06DTA_1071-0:0.0.0*255(1EBZ0123456789)1-0:96.1.0*255(1EBZ0123456789)1-0:1.8.0*255(000002.66313813*kWh)1-0:1.8.1*255(000000.999*kWh)1-0:1.8.2*255(000001.664*kWh)1-0:2.8.0*255(000002.15200000*kWh)1-0:16.7.0*255(001465.71*W)1-0:36.7.0*255(001397.00*W)1-0:56.7.0*255(000059.80*W)1-0:76.7.0*255(000008.91*W)1-0:32.7.0*255(231.6*V)1-0:52.7.0*255(234.3*V)1-0:72.7.0*255(233.7*V)1-0:96.5.0*255(001C0104)0-0:96.8.0*255(00000876)!/`

- find data point info in the [manual](https://github.com/philippoo66/eBZaehler/blob/main/manual/BA_eBZ_DD3_Rev02_2017-05-04.pdf)
- comfortably view, zoom and scroll the generated with the [CsvViewer](https://github.com/philippoo66/eBZaehler/tree/main/CsvViewer)

![grafik](https://github.com/philippoo66/eBZaehler/assets/122479122/a92f0c0c-418c-4ce1-a969-28f99649de17)


