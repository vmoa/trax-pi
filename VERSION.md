# T-Rax Version History

| Version | Date       | Notes |
|---------|------------|-------|
| v.1.0.7 | 2021-10-17 | Fixed toggleFob() roof logic |
|         |            | Increased fob_wait to 3 seconds |
|         |            | Better roof position reporting |
|         |            | Added "confused" roof state |
| v.1.0.6 | 2021-09-28 | Replace toggleThrice() with fob.toggleFob(), using callbacks instead of a timer loop |
| v.1.0.5 | 2021-08-22 | In emergency override, checkPark toggles laser indefinitely, and updateBrowser reports actual park position |
| v.1.0.4 | 2021-07-11 | Added toggleThrice() to make sure fob activates roof |
|         |            | Updated installation instructions |
| v.1.0.3 | 2021-07-07 | Removed pedantic power checks |
|         |            | Created test plan |
|         |            | mount and roof should not be reverse logic |
|         |            | pulled custom relay symbol into library |
|         |            | pass version to browser and report on connect |
| v.1.0.2 | 2021-06-05 | created service start script |
|         |            | added connection count to ticker |
|         |            | add file locking to prevent multiple copiesA |
|         |            | lots of documentation updates |
|         |            | lots of schematic updates |
| v.1.0   | 2021-04-25 | Released version 1.0; see `git log` for previous |
