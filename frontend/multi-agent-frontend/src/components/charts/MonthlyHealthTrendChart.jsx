
import React, { useEffect, useMemo, useState } from "react";
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
import { getLastMonthHealth } from "../../services/api";

function HeartRateChart() {
  const [heartRateData, setHeartRateData] = useState([]);
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMonthlyHealth = async () => {
      try {
        setLoading(true);
        const rows = await getLastMonthHealth();

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
              time: d.toLocaleDateString(undefined, { month: "short" }),
              heartRate: Number(r.heart_rate),
              systolic: Number(r.bp_systolic),
              diastolic: Number(r.bp_diastolic),
              timestamp: r.timestamp,
            };
          })
          .filter((p) => Number.isFinite(p.heartRate) || Number.isFinite(p.systolic) || Number.isFinite(p.diastolic));

        setHeartRateData(chartData);
        setConnected(true);
      } catch (err) {
        console.error("Failed to load monthly health:", err);
        setConnected(false);
      } finally {
        setLoading(false);
      }
    };

    loadMonthlyHealth();
  }, []);

  const currentBPM =
    heartRateData.length > 0
      ? heartRateData[heartRateData.length - 1].heartRate
      : "--";

  const chart = useMemo(() => heartRateData.slice(-30), [heartRateData]);

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6">
      
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white">
          Monthly Health Trend {connected ? "🟢" : "🔴"}
        </h3>
        <Zap className="w-5 h-5 text-cyan-400 animate-pulse" />
      </div>

      {loading ? (
        <div className="h-[250px] w-full rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-sm text-gray-300">
          Loading monthly trend…
        </div>
      ) : chart.length === 0 ? (
        <div className="h-[250px] w-full rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-sm text-gray-300">
          Please enter your health data daily to see your monthly heart rate and blood pressure trend.
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={chart}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />

            {/* <XAxis
              dataKey="time"
              stroke="rgba(255,255,255,0.5)"
              tick={{ fontSize: 12 }}
            /> */}
            <XAxis
  dataKey="time"
  stroke="rgba(255,255,255,0.5)"
  interval={Math.ceil(chart.length / 7)} // reduces clutter
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
              dataKey="heartRate"
              stroke="#06b6d4"
              strokeWidth={3}
              dot={false}
              isAnimationActive={false}
            />

            <Line
              type="monotone"
              dataKey="systolic"
              stroke="#f43f5e"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />

            <Line
              type="monotone"
              dataKey="diastolic"
              stroke="#fb7185"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      )}

      {/* <div className="mt-4 text-center p-3 bg-white/5 rounded-lg">
        <div className="text-sm text-gray-400">
          Current BPM:{" "}
          <span className="text-cyan-400 font-semibold text-lg">
            {currentBPM}
          </span>
        </div>
      </div> */}
      <div className="mt-4 text-center p-3 bg-white/5 rounded-lg">
  <p className="text-sm text-gray-400">
    💡 Tip: Stay hydrated and take short walks throughout the day to keep your heart healthy!
  </p>
</div>
    </div>
  );
}

export default HeartRateChart;