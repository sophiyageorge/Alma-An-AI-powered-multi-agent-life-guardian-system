
import React, { useEffect, useMemo, useState } from "react";
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
import { getLastWeekHealth } from "../../services/api";

function BloodPressureChart() {
  const [bpHistory, setBpHistory] = useState([]);
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadWeeklyBp = async () => {
      try {
        setLoading(true);
        const rows = await getLastWeekHealth();

        const sorted = Array.isArray(rows)
          ? [...rows].sort(
              (a, b) => new Date(a?.timestamp ?? 0) - new Date(b?.timestamp ?? 0)
            )
          : [];

        const chartData = sorted
          .filter((r) => r?.timestamp)
          .map((r) => {
            const d = new Date(r.timestamp);
            return {
              time: d.toLocaleDateString(undefined, { weekday: "short" }),
              systolic: Number(r.bp_systolic),
              diastolic: Number(r.bp_diastolic),
              heartRate: Number(r.heart_rate),
              timestamp: r.timestamp,
            };
          })
          .filter((p) => Number.isFinite(p.systolic) && Number.isFinite(p.diastolic));

        setBpHistory(chartData);
        setConnected(true);
      } catch (err) {
        console.error("Failed to load weekly BP:", err);
        setConnected(false);
      } finally {
        setLoading(false);
      }
    };

    loadWeeklyBp();
  }, []);

  const chart = useMemo(() => bpHistory.slice(-7), [bpHistory]);

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-rose-500/10 to-pink-500/10 backdrop-blur-xl border border-rose-500/20 rounded-2xl p-6">
      
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white">
          Weekly Health Chart {connected ? "🟢" : "🔴"}
        </h3>
        <Heart className="w-5 h-5 text-rose-400 animate-pulse" />
      </div>

      {loading ? (
        <div className="h-[250px] w-full rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-sm text-gray-300">
          Loading weekly trend…
        </div>
      ) : chart.length === 0 ? (
        <div className="h-[250px] w-full rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-sm text-gray-300">
          Please enter your health data daily to see your weekly blood pressure and heart rate trend.
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={chart}>
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

            <Area
              type="monotone"
              dataKey="heartRate"
              stroke="#22d3ee"
              fill="#22d3ee"
              fillOpacity={0.12}
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      )}
   <div className="mt-4 text-center p-3 bg-white/5 rounded-lg">
      <div className="mt-4 flex gap-4 text-sm justify-center p-3 bg-white/5 rounded-lg">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-rose-400 rounded-full"></span>
          <span className="text-gray-300">Systolic</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-pink-400 rounded-full"></span>
          <span className="text-gray-300">Diastolic</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-cyan-400 rounded-full"></span>
          <span className="text-gray-300">Heart Rate</span>
        </div>
        </div>
      </div>
  </div>
  );
}

export default BloodPressureChart;

    
