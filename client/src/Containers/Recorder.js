import { useState } from "react";
import { ReactMic } from "react-mic";

const Recorder = ({ sendAudio }) => {
  // const [blob, setBlob] = useState(null);
  const [record, setRecord] = useState(false);

  const startRecording = () => {
    setRecord(true);
  };

  const stopRecording = () => {
    setRecord(false);
  };

  const onData = (recordedBlob) => {
    // console.log("chunk of real-time data is: ", recordedBlob);
    // console.log(recordedBlob)
    // sendAudio(recordedBlob)
  };

  const onStop = (recordedBlob) => {
    // console.log('recordedBlob is: ', recordedBlob);
    sendAudio(recordedBlob);
  };
  return (
    <div>
      <ReactMic
        record={record}
        mimeType="audio/wav"
        className="sound-wave"
        onStop={onStop}
        onData={onData}
        strokeColor="#000000"
        timeSlice={30000}
        backgroundColor="#FF4081"
      />
      <button onClick={startRecording} type="button">
        Start
      </button>
      <button onClick={stopRecording} type="button">
        Stop
      </button>
    </div>
  );
};
export default Recorder;
