# How yaw rate is measured
In automotive systems this comes from a MEMS gyroscope (usually part of the ESC/ABS sensor cluster, sitting near the vehicle's center). A MEMS gyro has a tiny vibrating mass; when the sensor rotates, the Coriolis effect deflects that vibrating mass sideways, and the deflection is proportional to angular velocity. So the sensor outputs angular rate directly and continuously — it's a physical measurement, not a computed derivative of two angle readings.

This is actually the same physical principle as the gyroscope in your ImuData payload (roll_rate, pitch_rate, yaw_rate — all raw gyro readings). OdometryAngularRates is essentially the same underlying kind of measurement, just possibly a different/dedicated gyro in the odometry sensor path, offset-corrected as discussed.

