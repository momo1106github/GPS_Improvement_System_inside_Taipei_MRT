function accelerometer() {
  console.log("accelerometer");
  if ("Accelerometer" in window) {
    console.log("Accelerometer is in window");
    // The `Accelerometer` interface is supported by the browser.
    let accelerometer = null;
    try {
      accelerometer = new Accelerometer({ frequency: 10 });
      accelerometer.onerror = (event) => {
        // Handle runtime errors.
        if (event.error.name === "NotAllowedError") {
          console.log("Permission to access sensor was denied.");
        } else if (event.error.name === "NotReadableError") {
          console.log("Cannot connect to the sensor.");
        }
      };
      accelerometer.onreading = (e) => {
        console.log(e);
      };
      accelerometer.start();
    } catch (error) {
      // Handle construction errors.
      if (error.name === "SecurityError") {
        console.log(
          "Sensor construction was blocked by the Permissions Policy."
        );
      } else if (error.name === "ReferenceError") {
        console.log("Sensor is not supported by the User Agent.");
      } else {
        throw error;
      }
    }
  } else {
    console.log("nonononon");
  }
}

export default accelerometer;
