import axios from "axios";
import { useState } from "react";

const useRoute = () => {
  const [lng, setLng] = useState(121.573145);
  const [lat, setLat] = useState(24.998241);
  const development = process.env.NODE_ENV !== 'production'  
  const url = (development) ? "http://localhost:5000/audio":"https://obscure-spire-00084.herokuapp.com/audio";
  // console.log("development: ", development);

  const sendAudio = async (blob) => {
    let formData = new FormData();
    formData.append("wav_file", blob.blob);
    // console.log(blob);
    const result = await axios.post("/audio", formData, {
      headers: {
        Accept: "*/*",
        "Content-Type": "multipart/form-data",
      },
    });

    setLng(parseFloat(result.data[0]));
    setLat(parseFloat(result.data[1]));
  };

  const sendPic = async (imgSrc) =>{
    let formData = new FormData();
    const file = dataURLtoFile(imgSrc);
    formData.append('image_file', file);
    // console.log(formData.get("image_file"));
    const result = await axios.post("/image", formData, {
      headers: {
        'Content-Type': `multipart/form-data;`,
      }
    });
    console.log(result);
  }

  const sendBearing = async (bearing) =>{
    console.log("send Bearing", bearing);
    const result = await axios.post("/bearing", { bearing: bearing });
    console.log(result);
  }


  const dataURLtoFile = (dataurl, filename) => {
    const arr = dataurl.split(',')
    const mime = arr[0].match(/:(.*?);/)[1]
    const bstr = atob(arr[1])
    let n = bstr.length
    const u8arr = new Uint8Array(n)
    while (n) {
      u8arr[n - 1] = bstr.charCodeAt(n - 1)
      n -= 1 // to make eslint happy
    }
    return new File([u8arr], filename, { type: mime })
  }

  return { lng, lat, sendAudio, sendPic, sendBearing };
};
export default useRoute;
