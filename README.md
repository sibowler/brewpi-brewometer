These brewpi and other files have been modified to support the Tilt Hydrometer.

#NOTE: Upgrading from previous Brewometer install.

The references to Brewometer have been changed to Tilt. As such, if you are updating from an existing install, you will need to do the following:

1. Rename `/home/brewpi/brewometer` directory to `/home/brewpi/tiltHydrometer`
2. Ensure the existing Brewometer.py file has been deleted (note the code will still work if this file remains - this is just a cleanup step).

#Setup & Testing

Ensure you are updated to the latest version of Brewpi using the update script in the `brewpi-tools` folder.

On the raspberry pi you need to install the bluez bnd python-bluez luetooth modules to enable communication with the Tilt Hydrometer.

	sudo apt-get install bluez python-bluez python-scipy python-numpy libcap2-bin

Then you need to enable python to query bluetooth without being root.

	sudo setcap cap_net_raw+eip $(eval readlink -f `which python`)

Test that you've now enabled a connection by running the utility in the tiltHydrometer-test folder (this should not be run as root to test that we've enabled the appropriate permissions)
	
	python TiltHydrometerTest.py

If you see values against your colour Tilt Hydrometer, then the connection has been successful.

# Modifying Brewpi for Tilt Hydrometer logging

Ensure you have stopped any active logging.

The files in the `brewpi-web` folder should be copied to the `/var/www` directory. Ensure you fix the ownership once the files are copied over (`sudo chown -R www-data:www-data /var/www`)

The files in the `brewpi-script` folder should be copied to the `/home/brewpi` directory. Ensure you fix the ownership once the files are copied over (`sudo chown -R brewpi:brewpi /home/brewpi`)

Once the files have been copied across, you'll need to refresh the web interface and restart the script (button in top right-hand corner) to start logging. 


# Calibration:

To enable calibration for a Tilt Hydrometer create `GRAVITY.<colour>` or `TEMPERATURE.<colour>` files in the `/home/brewpi/tiltHydrometer` folder. Example files have been provided to show the syntax.

i.e. To calibrate a Red Tilt Hydrometer's temperature, a `TEMPERATURE.red` file should be created with the calibration settings inside.

## Note:
If this is not your first install of the Tilt Hydrometer modification, you will need to add the `python-scipy` and `python-numpy` libraries via apt-get. These libraries are used in the calibration function.

