import { useEffect, useRef, useState } from "react";
import mapboxgl from "!mapbox-gl"; // eslint-disable-line
import Map from "../Components/Map";
import Recorder from "./Recorder";
import useRoute from "../hooks/useRoute";
import useSensor from "../hooks/useSensor";
import Webcam from "./WebCam";
// import orientation from "../Functions/Orientation";

mapboxgl.accessToken =
  "pk.eyJ1Ijoic2hpbmUtY2hhbmciLCJhIjoiY2tvODhkdGw3MXU2dDJ2bHJrNDZmNHp6ZSJ9.-cSgmT-mTMNGs-to2jNmAw";

const MapController = () => {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const { lat, lng, id, sendAudio, sendPic, sendBearing } = useRoute();
  const [marker, setMarker] = useState(null);
  const [zoom, setZoom] = useState(13);
  const { bearing, orientation } = useSensor();
  const [lastBearing, setLastBearing] = useState(0);
  const bearingThreshhold = 10;
  useEffect(() => {
    setInterval(() => {
      saveData(bearing);
    }, 3000);
    setInterval(() => {
      downloadData();
    }, 6000);
  }, []);
  // const onMove = () => {
  //   setLng(map.current.getCenter().lng.toFixed(4));
  //   setLat(map.current.getCenter().lat.toFixed(4));
  //   setZoom(map.current.getZoom().toFixed(2));
  // };

  useEffect(() => {
    if (map.current) {
      map.current.flyTo({ center: [lng, lat], zoom: 14 });
      let newMarker = marker;
      setMarker(newMarker.setLngLat([lng, lat]).addTo(map.current));
    }
  }, [lng, lat, marker]);

  useEffect(() => {
    if (!map.current) return;
    map.current.setBearing(bearing);
    // console.log("bearing: ", bearing, lastBearing);
    if (Math.abs(bearing - lastBearing) > bearingThreshhold) {
      setLastBearing(bearing);
      sendBearing(bearing);
    }
  }, [bearing]);

  useEffect(() => {
    if (map.current) return; // initialize map only once
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [lng, lat],
      pitch: 30,
      zoom: zoom,
    });
    orientation();
    setMarker(
      new mapboxgl.Marker({
        color: "#1e90ff",
        draggable: true,
      })
        .setLngLat([lng, lat])
        .addTo(map.current)
    );
  });

  const saveData = (bearing) => {
    let data = JSON.parse(localStorage.getItem("data") || "[]");
    const nowData = {
      bearing: bearing,
      time: Date.now(),
      location: [lng, lat],
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
  return (
    <>
      <Map mapContainer={mapContainer} lng={lng} lat={lat} zoom={zoom}></Map>
      <Recorder sendAudio={sendAudio} />
      <Webcam sendPic={sendPic} />
    </>
  );
};
export default MapController;

// const setUsersLocation = (location) => {
//   renderMap([data.coords.longitude, data.coords.latitude]);
//   map.flyTo({ center: [location.longitude, location.latitude] });
// };
