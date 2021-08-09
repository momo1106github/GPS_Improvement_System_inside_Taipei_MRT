import { useState, useEffect } from "react";
import * as THREE from "three";
import { Gyroscope, AbsoluteOrientationSensor } from "motion-sensors-polyfill";

const useSensor = () => {
  const [bearing, setBearing] = useState(0);
  useEffect(() => {
    setInterval(() => {
      downloadData();
    }, 6000);
  }, []);
  const orientation = () => {
    const options = { frequency: 60 };
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
          // console.log(euler.setFromQuaternion(quaternion, "XYZ").z);
          const data = (180 / Math.PI * euler.setFromQuaternion(quaternion, "XYZ").z)
          setBearing(data);
          saveData(data)
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


  const saveData = (bearing) => {
    let data = JSON.parse(localStorage.getItem("data") || "[]");
    console.log(bearing)
    const nowData = {
      bearing: bearing,
      time: Date.now()
    };

    data = [...data, nowData];
    localStorage.setItem("data", JSON.stringify(data));
    console.log("localstorage:", data);
  };

  const downloadData = () => {
    let data = localStorage.getItem("data");
    let downloadData = new Blob([data], { type: "text/csv" });
    let csvURL = window.URL.createObjectURL(downloadData);
    let tempLink = document.createElement("a");
    tempLink.href = csvURL;
    let count = localStorage.getItem("count") || "0";
    count = parseInt(count) + 1;
    localStorage.setItem("count", count);
    tempLink.setAttribute("download", `${count}.csv`);
    tempLink.click();
    localStorage.setItem("data", []);
  };
  return {
    bearing,
    orientation,
  };
};

export default useSensor;
