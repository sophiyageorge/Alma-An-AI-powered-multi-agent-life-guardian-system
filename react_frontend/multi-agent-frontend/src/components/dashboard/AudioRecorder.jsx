import React, { useState, useRef } from "react";

const AudioRecorder = ({ onTranscription }) => {
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // Start recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/mp4" });
        const url = URL.createObjectURL(audioBlob);
        setAudioURL(url);

        // Send to FastAPI endpoint
        const formData = new FormData();
        formData.append("file", audioBlob, "recording.mp4");

        try {
          const response = await fetch("http://localhost:8000/stt/transcribe", {
            method: "POST",
            body: formData,
          });
          const data = await response.json();
          onTranscription(data.text); // Send transcript back to parent
        } catch (err) {
          console.error("Error sending audio to STT API:", err);
        }
      };

      mediaRecorderRef.current.start();
      setRecording(true);
    } catch (err) {
      console.error("Microphone access denied:", err);
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  return (
    <div style={{ padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
      <button
        onClick={recording ? stopRecording : startRecording}
        style={{
          padding: "10px 20px",
          backgroundColor: recording ? "#e74c3c" : "#2ecc71",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      {audioURL && (
        <div style={{ marginTop: "10px" }}>
          <audio controls src={audioURL} />
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;