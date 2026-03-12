import React, { useState, useRef, useEffect } from "react";
import { getAuthHeadersform, getJournal } from "../../services/api";
import { Sparkles, Mic, Square, Heart, Lightbulb, Calendar } from "lucide-react";

function parseJournalResponse(text) {
  if (!text) return { intro: "", tips: [], closing: "" };
  const lines = text.split("\n").filter(Boolean);
  const tips = [];
  const introLines = [];
  const closingLines = [];
  let inTips = false;

  lines.forEach((line) => {
    const tipMatch = line.match(/^\d+\.\s+(.*)/);
    if (tipMatch) {
      inTips = true;
      tips.push(tipMatch[1]);
    } else if (inTips) {
      closingLines.push(line);
    } else {
      introLines.push(line);
    }
  });

  return {
    intro: introLines.join(" "),
    tips,
    closing: closingLines.join(" "),
  };
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString("en-US", {
    weekday: "long", month: "long", day: "numeric",
  });
}

const AudioRecorder = ({ userId, onTranscription }) => {
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [journal, setJournal] = useState(null);
  const [loading, setLoading] = useState(true);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    const fetchJournal = async () => {
      try {
        const data = await getJournal();
        setJournal(data);
      } catch (err) {
        console.error("Error fetching journal:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchJournal();
  }, []);

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

        const formData = new FormData();
        formData.append("file", audioBlob, "recording.mp4");

        try {
          const response = await fetch("http://16.170.245.94:8000/stt/transcribe", {
            method: "POST",
            body: formData,
            headers: getAuthHeadersform(),
          });
          const data = await response.json();
          onTranscription && onTranscription(data.text);
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

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  const parsed = journal ? parseJournalResponse(journal.llm_response) : null;

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-white/20 hover:shadow-2xl transition-all duration-500">

      {/* Shimmer overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-200%] animate-shimmer pointer-events-none" />

      {/* Header */}
      <div className="flex flex-wrap items-center gap-3 mb-6">
        <div className="p-2 bg-gradient-to-br from-violet-400 to-fuchsia-500 rounded-xl shadow-lg shadow-violet-500/30">
          <Heart className="w-5 h-5 text-white" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-white">Daily Journal</h2>
          {journal?.date_created && (
            <p className="text-xs text-gray-400 flex items-center gap-1 mt-0.5">
              <Calendar className="w-3 h-3" />
              {formatDate(journal.date_created)}
            </p>
          )}
        </div>
        <div className="ml-auto flex items-center gap-1 px-3 py-1 bg-violet-500/20 border border-violet-500/30 rounded-full">
          <Sparkles className="w-3 h-3 text-violet-400 animate-pulse" />
          <span className="text-xs text-violet-300">AI Curated</span>
        </div>
      </div>

      {/* Journal AI Response */}
      {loading ? (
        <div className="space-y-3 mb-6">
          {[90, 75, 100, 80].map((w, i) => (
            <div
              key={i}
              className="h-3 rounded-full bg-white/5 animate-pulse"
              style={{ width: `${w}%`, animationDelay: `${i * 150}ms` }}
            />
          ))}
        </div>
      ) : parsed && (
        <div className="mb-6 space-y-4">

          {/* Intro */}
          {parsed.intro && (
            <div className="relative bg-gradient-to-br from-white/5 to-white/10 border border-white/10 rounded-xl p-4 hover:border-white/20 transition-all duration-300">
              <div className="absolute inset-0 bg-gradient-to-br from-violet-500/5 to-fuchsia-500/5 rounded-xl" />
              <p className="relative text-sm text-gray-300 leading-relaxed italic">
                "{parsed.intro}"
              </p>
            </div>
          )}

          {/* Tips */}
          {parsed.tips.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center gap-2 px-1">
                <Lightbulb className="w-3.5 h-3.5 text-violet-400" />
                <span className="text-xs font-semibold text-violet-300 uppercase tracking-wider">Suggestions</span>
              </div>
              {parsed.tips.map((tip, i) => (
                <div
                  key={i}
                  className="group flex items-start gap-3 bg-gradient-to-br from-white/5 to-white/10 border border-white/10 rounded-xl p-3 hover:border-white/20 hover:scale-[1.01] transition-all duration-300"
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-violet-500/10 to-fuchsia-500/10 opacity-0 group-hover:opacity-100 rounded-xl transition-opacity duration-300 pointer-events-none" />
                  <span className="flex-shrink-0 w-5 h-5 rounded-full bg-violet-500/20 border border-violet-500/30 text-violet-400 text-xs font-semibold flex items-center justify-center mt-0.5">
                    {i + 1}
                  </span>
                  <p className="text-xs text-gray-300 leading-relaxed">{tip}</p>
                </div>
              ))}
            </div>
          )}

          {/* Closing */}
          {parsed.closing && (
            <div className="pt-3 border-t border-white/10">
              <p className="text-xs text-gray-400 leading-relaxed">{parsed.closing}</p>
            </div>
          )}
        </div>
      )}

      {/* Divider */}
      <div className="flex items-center gap-3 mb-6">
        <div className="flex-1 h-px bg-white/10" />
        <span className="text-xs text-gray-500 uppercase tracking-widest">New Entry</span>
        <div className="flex-1 h-px bg-white/10" />
      </div>

      {/* Mic Section */}
      <div className="flex flex-col items-center gap-4">
        <div className="relative">
          {/* Ripple rings when recording */}
          {recording && (
            <>
              <span className="absolute inset-0 rounded-full bg-red-500/20 animate-ping" />
              <span className="absolute -inset-3 rounded-full bg-red-500/10 animate-ping" style={{ animationDelay: "0.3s" }} />
            </>
          )}
          <button
            onClick={recording ? stopRecording : startRecording}
            className={`relative w-20 h-20 rounded-full flex items-center justify-center transition-all duration-300 shadow-lg
              ${recording
                ? "bg-gradient-to-br from-red-500 to-rose-600 shadow-red-500/30 scale-110 hover:scale-105"
                : "bg-gradient-to-br from-violet-500 to-fuchsia-600 shadow-violet-500/30 hover:scale-110 hover:shadow-violet-500/50"
              }`}
          >
            {recording
              ? <Square className="w-7 h-7 text-white fill-white" />
              : <Mic className="w-7 h-7 text-white" />
            }
          </button>
        </div>

        <span className={`text-sm font-medium transition-colors duration-300 ${recording ? "text-red-400 animate-pulse" : "text-gray-400"}`}>
          {recording ? "● Recording... tap to stop" : "Tap to speak your thoughts"}
        </span>

        {audioURL && (
          <div className="w-full bg-gradient-to-br from-white/5 to-white/10 border border-white/10 rounded-xl p-3 hover:border-white/20 transition-all duration-300">
            <audio controls src={audioURL} className="w-full h-8" />
          </div>
        )}
      </div>
    </div>
  );
};

export default AudioRecorder;
// import React, { useState, useRef, useEffect } from "react";
// import { getAuthHeaders } from "../../services/api";
// import { getJournal } from "../../services/api";


// const AudioRecorder = ({ userId, onTranscription }) => {
//   const [recording, setRecording] = useState(false);
//   const [audioURL, setAudioURL] = useState(null);
//   const mediaRecorderRef = useRef(null);
//   const audioChunksRef = useRef([]);

//   useEffect(() => {
//     // Fetch journal entry on mount (optional, can be used to display existing entry)
//     const fetchJournal = async () => {
//       try { 
//         const data = await getJournal();
//         console.log("Today's journal entry:", data);
//       }
//       catch (err) {
//         console.error("Error fetching journal entry:", err);
//       }
//     };

//     fetchJournal();
//   }, []);

//   // Start recording
//   const startRecording = async () => {
//     try {
//       const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//       mediaRecorderRef.current = new MediaRecorder(stream);
//       audioChunksRef.current = [];

//       mediaRecorderRef.current.ondataavailable = (event) => {
//         if (event.data.size > 0) audioChunksRef.current.push(event.data);
//       };

//       mediaRecorderRef.current.onstop = async () => {
//         const audioBlob = new Blob(audioChunksRef.current, { type: "audio/mp4" });
//         const url = URL.createObjectURL(audioBlob);
//         setAudioURL(url);

//         // Send audio + userId to FastAPI endpoint
//         const formData = new FormData();
//         formData.append("file", audioBlob, "recording.mp4");
//         // formData.append("user_id", userId); // <-- include user ID

//         try {
//           const response = await fetch("http://localhost:8000/stt/transcribe", {
//             method: "POST",
//             body: formData,
//             headers: getAuthHeaders(), // <-- include auth headers
//           });
//           const data = await response.json();
//           onTranscription && onTranscription(data.text); // Send transcript back to parent
//         } catch (err) {
//           console.error("Error sending audio to STT API:", err);
//         }
//       };

//       mediaRecorderRef.current.start();
//       setRecording(true);
//     } catch (err) {
//       console.error("Microphone access denied:", err);
//     }
//   };

//   // Stop recording
//   const stopRecording = () => {
//     if (mediaRecorderRef.current) {
//       mediaRecorderRef.current.stop();
//       setRecording(false);
//     }
//   };

//   return (
//     <div style={{ padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
//       <button
//         onClick={recording ? stopRecording : startRecording}
//         style={{
//           padding: "10px 20px",
//           backgroundColor: recording ? "#e74c3c" : "#2ecc71",
//           color: "#fff",
//           border: "none",
//           borderRadius: "4px",
//           cursor: "pointer",
//         }}
//       >
//         {recording ? "Stop Recording" : "Start Recording"}
//       </button>

//       {audioURL && (
//         <div style={{ marginTop: "10px" }}>
//           <audio controls src={audioURL} />
//         </div>
//       )}
//     </div>
//   );
// };

// export default AudioRecorder;
