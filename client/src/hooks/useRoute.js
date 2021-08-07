import axios from "axios";
import { useState, useEffect } from "react";

const useRoute = () => {
  const [lng, setLng] = useState(121.573145);
  const [lat, setLat] = useState(24.998241);
  const development = process.env.NODE_ENV !== "production";
  const getUserId = async () => {
    const { data } = await axios.get("/id");
    console.log("getUserId", data);
    id = data;
  };
  useEffect(() => {
    const getUserId = async () => {
      const { data } = await axios.get("/id");
      console.log("getUserId", data);
      id = data;
    };
    getUserId();
  }, []);

  let id = null;

  const sendAudio = async (blob) => {
    let formData = new FormData();
    formData.append("wav_file", blob.blob);

    console.log("id:", id);
    const result = await axios.post("/audio", formData, {
      headers: {
        Accept: "*/*",
        "Content-Type": "multipart/form-data",
        Authorization: `Basic ${Buffer.from(`111:${id}`, "utf8").toString(
          "base64"
        )}`,
      },
    });

    setLng(parseFloat(result.data[0]));
    setLat(parseFloat(result.data[1]));
  };

  const sendPic = async (imgSrc) => {
    let formData = new FormData();
    const file = dataURLtoFile(imgSrc);
    formData.append("image_file", file);

    // console.log(formData.get("image_file"));
    const result = await axios.post("/image", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Basic ${Buffer.from(`111:${id}`, "utf8").toString(
          "base64"
        )}`,
      },
    });
    console.log(result);
  };

  const sendBearing = async (bearing) => {
    if (!id) await getUserId();
    console.log("send Bearing", bearing);
    
    const result = await axios.post(
      "/bearing",
      { bearing: bearing },
      {
        headers: {
          Authorization: `Basic ${Buffer.from(`111:${id}`, "utf8").toString(
            "base64"
          )}`,
        },
      }
    );
    console.log(result);
  };

  const dataURLtoFile = (dataurl, filename) => {
    const arr = dataurl.split(",");
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n) {
      u8arr[n - 1] = bstr.charCodeAt(n - 1);
      n -= 1; // to make eslint happy
    }
    return new File([u8arr], filename, { type: mime });
  };

  

  return { lng, lat, sendAudio, sendPic, sendBearing, getUserId };
};
export default useRoute;
