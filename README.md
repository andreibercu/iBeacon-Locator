# Django Web Interface for an iBeacon Localization System

This is a web application used as part of an indoor localization system I developed. The system also contains iBeacon devices (bluetooth LE signal transmitters) and Raspberry Pi single board computers, which act as signal receivers. The web application collects the signal power data from the Raspberry Pis, runs the localization algorithm and updates the beacon location in the web interface in real time.  

The application is developed in Python using the Django framework.

The most important files in the project repo are located in the src/ibeaconapp directory:
  - urls.py - containing url routes;
  - models.py - containing data 'Model' definitions;
  - views.py - containing 'Controller' classes and functions. BeaconLocationView is the most important Controller, providing real time information about the beacon locations;
  - beaconlocator.py - containing the algorithm for data analysis and beacon localization, used in the BeaconLocationView Controller;
  - areaexplorer.py - part of the localization algorithm, used by the BeaconLocator class in beaconlocator.py . Given the estimated distances between the beacon transmitters and at least 3 receivers, it returns the estimated 2D location;
  - rssifilters.py - containing a signal power filtering function based on the Gaussian Mixture Model algorithm; also used in the BeaconLocator;
  - beacongeometry.py - not used anymore. It was also part of the beacon localization algorithm;
  - templates/ibeaconapp/* - html templates. They also include js scripts. The most important is beacon_location.html, providing real time beacon location information by drawing location point coordinates on an image floor map (seriously, the javascript canvas y axis is upside down? who invented javascript?);
  - static/ibeaconapp/css/* - some basic css settings (I also used Bootstrap 4.0);
  - test_* - unit test files (trying to be a professional here!).
