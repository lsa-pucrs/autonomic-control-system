# Control Dense Optical Flow latency through camera resolution or image resolution

To use, run "control_opt_flow.py" with the following arguments:

* Control variable (camera_res | image_res)
* Setpoint (e.g. 0.1)
* Proportional gain
* Integral gain

control_opt_flow.py will spawn the appropriate DoF application and log experiment time, control signal and process output in a text file named "logfile.txt".