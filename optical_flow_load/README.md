# Control CPU load through update rate, camera resolution or image resolution

To use, run "control_opt_flow.py" with the following arguments:

* Control variable (update_rate | camera_res | image_res)
* Setpoint (e.g. 50)
* Proportional gain
* Integral gain

control_opt_flow.py will spawn the appropriate DoF application and log experiment time, control signal and process output in a text file named "logfile.txt".