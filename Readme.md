To get Temperature value, use the smaple code

>>> import Temperature
>>> temp_sensor = Temperature.MLX90614()
>>> temp_sensor.get_avg_temp()
value: 96.60560

To get SpO2 and heart beat value:

>>> import max30102
>>> import hrcalc
>>> max_obj = max30102.MAX30102()
>>> red_data, ir_data = max_obj.read_sequential()
>>> hrcalc.calc_hr_and_spo2(ir_data[:100], red_data[:100])
(66, True, 95, True)
