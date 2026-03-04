// import React, { useEffect, useRef, useState } from "react";
import { Activity, TrendingUp } from "lucide-react";

export default function HeartRateCardTest() {
  const [heartRate, setHeartRate] = useState(0);
  const [status, setStatus] = useState("Connecting...");
  const [mounted, setMounted] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    setMounted(true);
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const connectWebSocket = () => {
    const ws = new WebSocket("ws://localhost:8000/realtime/ws");
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("HeartRate WebSocket connected");
      setStatus("Live");
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        if (msg.heart_rate) {
          setHeartRate(Number(msg.heart_rate));
        }
      } catch (err) {
        console.error("Parse error:", err);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket closed. Reconnecting...");
      setStatus("Reconnecting...");
      setTimeout(connectWebSocket, 2000);
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
      ws.close();
    };
  };

  const getCondition = () => {
    if (heartRate === 0) return "Waiting...";
    if (heartRate < 60) return "Low";
    if (heartRate > 100) return "High";
    return "Normal";
  };

  const getConditionColor = () => {
    if (heartRate < 60) return "text-yellow-400";
    if (heartRate > 100) return "text-red-400";
    return "text-green-400";
  };

  return (
    <div
      className={`group relative overflow-hidden bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 transition-all duration-500 hover:scale-[1.02] ${
        mounted ? "opacity-100 translate-x-0" : "opacity-0 translate-x-20"
      }`}
      style={{ transitionDelay: "300ms" }}
    >
      <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/10 rounded-full -mr-16 -mt-16 group-hover:scale-150 transition-transform duration-500"></div>

      <div className="relative">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-cyan-500/20 rounded-xl animate-pulse">
              <Activity className="w-6 h-6 text-cyan-400" />
            </div>
            <h3 className="text-lg font-semibold text-white">
              Heart Rate
            </h3>
          </div>

          <div className={`flex items-center gap-1 text-sm ${getConditionColor()}`}>
            <TrendingUp className="w-4 h-4" />
            <span>{getCondition()}</span>
          </div>
        </div>

        {/* Heart Rate Value */}
        <div className="flex items-baseline gap-3 mb-3">
          <div className="text-5xl font-bold text-white transition-all duration-300 group-hover:text-cyan-300">
            {heartRate}
          </div>
          <div className="text-cyan-300 text-lg">bpm</div>
        </div>

        {/* Status */}
        <div className="text-xs text-gray-400 mb-3">
          Status: {status}
        </div>

        {/* Quote Section */}
        <div className="bg-white/5 rounded-lg p-3 hover:bg-white/10 transition-colors duration-300">
          <div className="text-sm font-semibold text-white">
            Every heartbeat is a reminder that you're alive and thriving.
          </div>
        </div>
      </div>
    </div>
  );
}