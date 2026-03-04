

import React, { useEffect, useRef, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Zap } from "lucide-react";

function HeartRateChart() {
  const [heartRateData, setHeartRateData] = useState([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null); // prevent multiple connections

  useEffect(() => {
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
      console.log("WebSocket connected");
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        if (msg.heart_rate && msg.timestamp) {
          const formattedTime = new Date(msg.timestamp).toLocaleTimeString();

          const newPoint = {
            time: formattedTime,
            rate: Number(msg.heart_rate),
          };

          setHeartRateData((prev) => {
            const updated = [...prev, newPoint];
            return updated.slice(-30); // keep last 30 points
          });
        }
      } catch (err) {
        console.error("Parse error:", err);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket closed. Reconnecting...");
      setConnected(false);

      // Auto reconnect after 2 seconds
      setTimeout(() => {
        connectWebSocket();
      }, 2000);
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
      ws.close();
    };
  };

  const currentBPM =
    heartRateData.length > 0
      ? heartRateData[heartRateData.length - 1].rate
      : "--";

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6">
      
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white">
          Heart Rate Trend {connected ? "🟢" : "🔴"}
        </h3>
        <Zap className="w-5 h-5 text-cyan-400 animate-pulse" />
      </div>

      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={heartRateData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />

          <XAxis
            dataKey="time"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 12 }}
          />

          <YAxis
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 12 }}
            domain={["auto", "auto"]}
          />

          <Tooltip
            contentStyle={{
              backgroundColor: "rgba(15,23,42,0.95)",
              borderRadius: "12px",
              color: "#fff",
            }}
          />

          <Line
            type="monotone"
            dataKey="rate"
            stroke="#06b6d4"
            strokeWidth={3}
            dot={false}
            isAnimationActive={false}  // important for smooth real-time
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="mt-4 text-center p-3 bg-white/5 rounded-lg">
        <div className="text-sm text-gray-400">
          Current BPM:{" "}
          <span className="text-cyan-400 font-semibold text-lg">
            {currentBPM}
          </span>
        </div>
      </div>
    </div>
  );
}

export default HeartRateChart;