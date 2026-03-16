

import React, { useEffect, useRef, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Heart } from "lucide-react";

function BloodPressureChart() {
  const [bpHistory, setBpHistory] = useState([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);

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
      console.log("BP Chart WebSocket connected");
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        if (msg.bp_systolic && msg.bp_diastolic && msg.timestamp) {
          const formattedTime = new Date(msg.timestamp).toLocaleTimeString();

          const newPoint = {
            time: formattedTime,
            systolic: Number(msg.bp_systolic),
            diastolic: Number(msg.bp_diastolic),
          };

          setBpHistory((prev) => {
            const updated = [...prev, newPoint];
            return updated.slice(-20); // keep last 20 readings
          });
        }
      } catch (err) {
        console.error("BP chart parse error:", err);
      }
    };

    ws.onclose = () => {
      console.log("BP Chart WebSocket closed. Reconnecting...");
      setConnected(false);
      setTimeout(connectWebSocket, 2000);
    };

    ws.onerror = (err) => {
      console.error("BP Chart WebSocket error:", err);
      ws.close();
    };
  };

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-rose-500/10 to-pink-500/10 backdrop-blur-xl border border-rose-500/20 rounded-2xl p-6">
      
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white">
          Blood Pressure Trend {connected ? "🟢" : "🔴"}
        </h3>
        <Heart className="w-5 h-5 text-rose-400 animate-pulse" />
      </div>

      <ResponsiveContainer width="100%" height={250}>
        <AreaChart data={bpHistory}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="rgba(255,255,255,0.1)"
          />

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
              border: "1px solid rgba(244,63,94,0.3)",
              borderRadius: "12px",
              color: "#fff",
            }}
          />

          <Area
            type="monotone"
            dataKey="systolic"
            stroke="#f43f5e"
            fill="#f43f5e"
            fillOpacity={0.3}
            isAnimationActive={false}
          />

          <Area
            type="monotone"
            dataKey="diastolic"
            stroke="#fb7185"
            fill="#fb7185"
            fillOpacity={0.2}
            isAnimationActive={false}
          />
        </AreaChart>
      </ResponsiveContainer>

      <div className="mt-4 flex gap-4 text-sm justify-center p-3 bg-white/5 rounded-lg">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-rose-400 rounded-full"></span>
          <span className="text-gray-300">Systolic</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-pink-400 rounded-full"></span>
          <span className="text-gray-300">Diastolic</span>
        </div>
      </div>
    </div>
  );
}

export default BloodPressureChart;

    
