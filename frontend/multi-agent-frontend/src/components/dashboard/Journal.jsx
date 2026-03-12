import React, { useState } from "react";
import AudioRecorder from "./AudioRecorder";

const App = () => {
  const [transcript, setTranscript] = useState("");

  return (
    <div>
      <h1>Audio Recorder with STT</h1>
      <AudioRecorder onTranscription={setTranscript} />
      {transcript && (
        <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ddd" }}>
          <h3>Transcription:</h3>
          <p>{transcript}</p>
        </div>
      )}
    </div>
  );
};

export default App;