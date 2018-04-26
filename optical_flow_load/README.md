# Control CPU load through update rate, camera resolution or image resolution

To use, run "control_opt_flow.py" with the following arguments:

* Control variable (update_rate | camera_res | image_res)
* Setpoint (e.g. 50)
* Proportional gain
* Integral gain

control_opt_flow.py will spawn the appropriate DoF application and log experiment time, control signal and process output in a text file named "logfile.txt".

The PI gains empirically found for each control variable were:

* Update rate:
** P = 0.0007
** I = 0.007

* Camera resolution:
** P = 1.5
** I = 1.5

* Image resolution:
** P = 2
** I = 2
