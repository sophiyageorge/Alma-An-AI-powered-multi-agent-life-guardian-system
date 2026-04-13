import React, { useState, useRef, useEffect } from "react";
import { getJournal, transcribeAudio } from "../../services/api";
import { Sparkles, Mic, Square, Heart, Calendar } from "lucide-react";

/* ------------------ SAFE JSON PARSER ------------------ */
function parseLLMResponse(data) {
  if (!data) return null;

  try {
    return typeof data === "string" ? JSON.parse(data) : data;
  } catch (e) {
    console.error("LLM parse error:", e);
    return null;
  }
}

/* ------------------ DATE FORMAT ------------------ */
function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });
}

const AudioRecorder = ({ onTranscription }) => {
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [journal, setJournal] = useState(null);
  const [loading, setLoading] = useState(true);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  const MAX_DURATION = 60 * 1000;

  /* ------------------ FETCH JOURNAL ------------------ */
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

  /* ------------------ RECORDING START ------------------ */
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunksRef.current.push(e.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        clearTimeout(timerRef.current);

        const blob = new Blob(audioChunksRef.current, { type: "audio/mp4" });
        const url = URL.createObjectURL(blob);

        setAudioURL(url);
        setRecording(false);

        try {
          const transcription = await transcribeAudio(blob);
          onTranscription?.(transcription);
        } catch (err) {
          console.error("Transcription failed:", err);
        }
      };

      mediaRecorderRef.current.start();
      setRecording(true);

      timerRef.current = setTimeout(() => {
        if (mediaRecorderRef.current?.state === "recording") {
          mediaRecorderRef.current.stop();
          alert("⏱️ Max recording time reached");
        }
      }, MAX_DURATION);

    } catch (err) {
      console.error("Mic error:", err);
    }
  };

  /* ------------------ STOP RECORDING ------------------ */
  const stopRecording = () => {
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    clearTimeout(timerRef.current);
    setRecording(false);
  };

  /* ------------------ PARSE JOURNAL ------------------ */
  const parsed = journal?.llm_response
    ? parseLLMResponse(journal.llm_response)
    : null;

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl border border-white/10 rounded-2xl p-6">

      {/* ---------------- HEADER ---------------- */}
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-gradient-to-br from-violet-400 to-fuchsia-500 rounded-xl">
          <Heart className="w-5 h-5 text-white" />
        </div>

        <div>
          <h2 className="text-xl font-bold text-white">Daily Journal</h2>

          {journal?.date_created && (
            <p className="text-xs text-gray-400 flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              {formatDate(journal.date_created)}
            </p>
          )}
        </div>

        <div className="ml-auto flex items-center gap-1 px-3 py-1 bg-violet-500/20 rounded-full">
          <Sparkles className="w-3 h-3 text-violet-400" />
          <span className="text-xs text-violet-300">AI</span>
        </div>
      </div>

      {/* ---------------- JOURNAL UI ---------------- */}
      {loading ? (
        <p className="text-gray-400 text-sm">Loading...</p>
      ) : parsed?.analysis && parsed?.response && (
        <div className="space-y-4">

          {/* Mood */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <p className="text-violet-300 text-sm font-semibold">
              Mood Analysis
            </p>

            <p className="text-gray-200 text-sm mt-2">
              <b>Mood:</b> {parsed.analysis.detected_mood}
            </p>

            <p className="text-gray-300 text-sm mt-1">
              <b>Themes:</b> {parsed.analysis.key_themes?.join(", ")}
            </p>
          </div>

          {/* Acknowledgment */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <p className="text-gray-200 text-sm">
              {parsed.response.acknowledgment}
            </p>
          </div>

          {/* Suggestions */}
          {parsed.response.suggestions?.length > 0 && (
            <div className="space-y-2">
              <p className="text-xs text-violet-300 uppercase">
                Suggestions
              </p>

              {parsed.response.suggestions.map((item, i) => (
                <div
                  key={i}
                  className="bg-white/5 border border-white/10 rounded-xl p-3"
                >
                  <p className="text-white text-sm font-semibold">
                    {item.title}
                  </p>
                  <p className="text-gray-300 text-xs">
                    {item.description}
                  </p>
                </div>
              ))}
            </div>
          )}

          {/* Closing */}
          <p className="text-gray-400 text-xs border-t border-white/10 pt-3">
            {parsed.response.closing_encouragement}
          </p>

        </div>
      )}

      {/* ---------------- MIC ---------------- */}
      <div className="mt-6 flex flex-col items-center gap-4">

        <button
          onClick={recording ? stopRecording : startRecording}
          className={`w-20 h-20 rounded-full flex items-center justify-center transition-all
            ${recording
              ? "bg-red-500"
              : "bg-gradient-to-br from-violet-500 to-fuchsia-600"
            }`}
        >
          {recording ? (
            <Square className="text-white" />
          ) : (
            <Mic className="text-white" />
          )}
        </button>

        <p className="text-sm text-gray-400">
          {recording ? "Recording..." : "Tap to speak"}
        </p>

        {audioURL && (
          <audio controls src={audioURL} className="w-full mt-2" />
        )}

      </div>
    </div>
  );
};

export default AudioRecorder;