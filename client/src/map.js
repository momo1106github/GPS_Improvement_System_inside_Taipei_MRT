import "https://api.mapbox.com/mapbox-gl-js/v2.1.1/mapbox-gl.js";
import * as THREE from "https://cdn.skypack.dev/three@0.129.0";

let map;
mapboxgl.accessToken = "pk.eyJ1Ijoic2hpbmUtY2hhbmciLCJhIjoiY2tvODhkdGw3MXU2dDJ2bHJrNDZmNHp6ZSJ9.-cSgmT-mTMNGs-to2jNmAw";
  

const initializeMap = () => {
  navigator.geolocation.getCurrentPosition((data) => {
    renderMap([data.coords.longitude, data.coords.latitude]);
  });
}

function renderMap(data) {
  map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v11",
    center: data,
    zoom: 15,
    pitch: 60,
    bearing: -10,
  });
}


const setUsersLocation = (location) => {
  renderMap([data.coords.longitude, data.coords.latitude]);
  map.flyTo({center: [location.longitude, location.latitude]});
}

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
        console.log(euler.setFromQuaternion(quaternion, 'XYZ').z);
        map.setBearing(45 * euler.setFromQuaternion(quaternion, 'XYZ').z);

        
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
}


const GPSImprovementSystem = () => {
    initializeMap();
    const apiPath = "http://localhost:5000/audio";
    const data = 
    while (true) {
      $.ajax({url: apiPath, succes: function(result) {
        
      }})
    }
}


GPSImprovementSystem();
// const notUsed = () => {
//   navigator.geolocation.getCurrentPosition((data) => {
//     renderMap([data.coords.longitude, data.coords.latitude]);
//   });
//   navigator.geolocation.watchPosition(
//     (data) => {
//       map.flyTo({
//         center: [data.coords.longitude, data.coords.latitude],
//       });
//     },
//     (error) => console.log(error),
//     {
//       enableHighAccuracy: true,
//     });
// }
// function accelerometer() {
//   console.log("accelerometer");
//   if ("Accelerometer" in window) {
//     console.log("Accelerometer is in window");
//     // The `Accelerometer` interface is supported by the browser.
//     let accelerometer = null;
//     try {
//       accelerometer = new Accelerometer({ frequency: 10 });
//       accelerometer.onerror = (event) => {
//         // Handle runtime errors.
//         if (event.error.name === "NotAllowedError") {
//           console.log("Permission to access sensor was denied.");
//         } else if (event.error.name === "NotReadableError") {
//           console.log("Cannot connect to the sensor.");
//         }
//       };
//       accelerometer.onreading = (e) => {
//         console.log(e);
//       };
//       accelerometer.start();
//     } catch (error) {
//       // Handle construction errors.
//       if (error.name === "SecurityError") {
//         console.log(
//           "Sensor construction was blocked by the Permissions Policy."
//         );
//       } else if (error.name === "ReferenceError") {
//         console.log("Sensor is not supported by the User Agent.");
//       } else {
//         throw error;
//       }
//     }
//   } else {
//     console.log("nonononon");
//   }
// }
