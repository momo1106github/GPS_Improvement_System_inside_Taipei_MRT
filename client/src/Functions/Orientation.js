import * as THREE from "three";

const orientation = () => {
  const options = { frequency: 60, referenceFrame: "device" };
  const sensor = new AbsoluteOrientationSensor(options);

  Promise.all([
    navigator.permissions.query({ name: "accelerometer" }),
    navigator.permissions.query({ name: "magnetometer" }),
    navigator.permissions.query({ name: "gyroscope" }),
  ]).then((results) => {
    if (results.every((result) => result.state === "granted")) {
      sensor.addEventListener("reading", () => {
        const euler = new THREE.Euler();
        const quaternion = new THREE.Quaternion(...sensor.quaternion);
        console.log(euler.setFromQuaternion(quaternion, "XYZ").z);
        // map.setBearing(45 * euler.setFromQuaternion(quaternion, "XYZ").z);
      });
      sensor.addEventListener("error", (event) => {
        if (event.error.name === "NotReadableError") {
          console.log("Sensor is not available.", event);
        }
      });
      sensor.start();
    } else {
      console.log("No permissions to use AbsoluteOrientationSensor.");
    }
  });
};
export default orientation;