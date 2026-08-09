# Main sensors

## Odometer

### Velocities - OdometryVelocities
Velocity vector in USK (environment sensor coordinate system) according to DIN70000  with confidence, variance and a timestamp.

| Field name                   | Type             | Description                                                      |
| ---------------------------- | ---------------- | -----------------------------------------------------------------|
| type                         | enum             | 0 = velocityX; 1 = velocityY;                                    |
| timestamp                    | uint64           | PTP timestamp, unit = us                                         |
| value                        | float32          | Value of velocity in defined direction of USK. unit = m/s        |
| variance                     | float32          | Variance of velocity in defined direction of USK, unit = (m/s)^2 |
| confidence                   | enum             | Validity of velocity in defined direction of USK                 |

> Confidence values interpretation:
> Valid = Signal available, quality requirements fullfilled,
> Best Guess = Signal available, degraded estimation with potential quality loss,
> Init = Initialisation not finished or signal not provided,
> Error = Internal failure
> ErrorInputData = Input data failure

### Angular rates - OdometryAngularRates
Angular rates are defined according to DIN 70000 sensor frame with variance and confidence and timestamp.

| Field name                   | Type             | Description                                                      |
| ---------------------------- | ---------------- | -----------------------------------------------------------------|
| type                         | enum             | 0 = yawRate;                                                     |
| timestamp                    | uint64           | PTP timestamp, unit = us                                         |
| angularrate                  | float32          | Offset corrected yawrate of vehicle. unit = rad/s                |
| variance                     | float32          | Upper estimate of variance of angular rate, unit = (rad/s)^2     |
| confidence                   | enum             | Validity of angular rate.                                        |

> Angular rate offset interpretation:
> Offset is estimated in standstill and kept until next standstill.

> Confiedence values interpretation:
> Valid = Signal available, quality requirements fullfilled,
> Best Guess = Signal available, degraded estimation with potential quality loss,
> Init = Initialisation not finished or signal not provided,
> Error = Internal failure
> ErrorInputData = Input data failure

