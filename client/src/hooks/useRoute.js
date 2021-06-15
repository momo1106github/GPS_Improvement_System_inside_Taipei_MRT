import axios from "axios";
import { useState } from "react";

const useRoute = () => {
  const [lng, setLng] = useState(121.573145);
  const [lat, setLat] = useState(24.998241);

  const sendAudio = async (blob) => {
    let formData = new FormData();
    formData.append("wav_file", blob.blob);
    const result = await axios.post("http://localhost:5000/audio", formData, {
      headers: {
        Accept: "*/*",
        "Content-Type": "multipart/form-data",
      },
    });

    setLng(parseFloat(result.data[0]));
    setLat(parseFloat(result.data[1]));
  };
  return { lng, lat, sendAudio };
};
export default useRoute;
