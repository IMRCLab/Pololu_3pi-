# Pololu 3pi+ RP2040 Robot Development Repository

In this branch a new way to select trajectories has been developed. Instead of changing the config file to choose a trajectory it is now possible to choose a trajectory via radio command.

When the robot starts a new image in the display appears:

```

 WAITING FOR 
  ______
 /|_||_\`.__
(   _    _ _\ 
=`-(_)--(_)-'
-- --- --- --- -
 TRAJECTORY

```

When this image appears the robot is waiting for a new trajectory command. The trajectory command is the same as the start_trajectory command, but the forth byte is set to true. In the start_trajectory command it is saved as the relative bit.

```c++
startTrajectoryCommand(bool relative, bool reversed, uint8_t trajectoryId, float timescale)
```

The other information which needs to be transmitted is the trajectory_id. This number corresponds to the list indices in the config.json file.

```json
{
    "trajectory" : ["unicycle_flatness.json","line.json","point.json"],
    "ID" : "0xe7",
    "Logging" : 0,
    "Gains" : [6.5,9.5,5.0],
    "Max Speed" : 6000,
    "Logging Interval" : 0.2,
    "Logging Time" : 10
}
```
After the trajectory_id has been processed the robot routine continuous as usual.
