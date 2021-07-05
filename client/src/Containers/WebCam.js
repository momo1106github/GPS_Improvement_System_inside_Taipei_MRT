import Webcam from "react-webcam";
import React, {useRef} from 'react';

const videoConstraints = {
    width: 1280,
    height: 720,
    // facingMode: { exact: "environment" }
    facingMode: "user"
  };

const WebCamContainer = ({sendPic}) =>{
  const webcamRef = React.useRef(null);
  const capture = React.useCallback(
    () => {
      const imageSrc = webcamRef.current.getScreenshot();
    //   console.log(imageSrc);
      sendPic(imageSrc);
    },
    [webcamRef]
  );

  return (
    <>
    <button onClick={capture}>Capture photo</button>
    <Webcam
        audio={false}
        height={720}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={1280}
        videoConstraints={videoConstraints}
    />
    </>
);
}

export default WebCamContainer;