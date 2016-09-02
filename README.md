# roadNet

roadNet is an application for managing a BS7666-compliant local street gazetteer (LSG).  It also handles Scottish Roadworks Register associated data and road assets.

----
## Quick start

roadNet ships with a demo database.  To give it a try:

*  Select the demo database:
    +  Click _roadNet > Change database location_
    +  Navigate to the roadNet plugin directory (typically _<username>/.qgis2/python/plugins/Roadnet_)
    +  Choose the _database_files/roadnet_demo.sqlite_ database
    +  Press _Apply_
*  Log in:
    +  Click _roadNet > Start roadNet_
    +  Enter username and password as _thinkwhere_, _thinkwhere_
*  Start using roadNet e.g.
    +  Use the Street Selector to select a street and get LSG information
    +  Use the Street Browser to browse records
    +  Export records in Scottish Data Transfer Format
    +  Use RAMP tools to add IDs to road assets

Alternatively, select the _roadnet_empty.sqlite_ to begin capturing your own data.

----
## Tests and continuous integration

roadNet comes with a test suite and continuous integration system using Shippable.  Commits pushed to the repository are automatically tested in the cloud.

Tests can also be run locally.  On Linux, this can be done by running the following from the Roadnet directory:

```
../Roadnet/bin/tests.sh
```

----
## Further information and support

See the [roadNet Manual](http://www.thinkwhere.com/files/4014/5572/6600/roadNet_Manual_-_edited_14-01-2016.pdf) for full information and instructions.

[thinkWhere](http://www.thinkwhere.com) offer a number of support options including training, QGIS training and database migrations.

Please direct any queries to [support@thinkwhere.com](mailto://support@thinkwhere.com).