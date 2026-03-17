

import React, { useState, useEffect, useRef } from "react";
import { Heart, TrendingUp } from "lucide-react";
import { getHealth } from "../../services/api";

function BloodPressureCard() {
  const [bpData, setBpData] = useState({
    bp_systolic: "--",
    bp_diastolic: "--",
  });

  const [pulseHeart, setPulseHeart] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [connected, setConnected] = useState(false);

 

  useEffect(() => {
    setMounted(true);

    const loadBloodPressure = async () => {
      try {
        const data = await getHealth();

        setBpData({
          bp_systolic: data.bp_systolic ?? "--",
          bp_diastolic: data.bp_diastolic ?? "--",
        });

        setConnected(true);
        setPulseHeart(true);
        setTimeout(() => setPulseHeart(false), 300);
      } catch (error) {
        console.error(error);
        setConnected(false);
      }
    };

    loadBloodPressure();
  }, []);
  

  const isHealthy =
    Number(bpData.bp_systolic) < 120 &&
    Number(bpData.bp_diastolic) < 80;

  return (
    <div
      className={`group relative overflow-hidden bg-gradient-to-br 
      from-rose-500/10 to-pink-500/10 backdrop-blur-xl 
      border border-rose-500/20 rounded-2xl p-6 
      transition-all duration-500 hover:scale-[1.02]
      ${mounted ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-20"}`}
    >
      <div className="relative">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div
              className={`p-3 bg-rose-500/20 rounded-xl transition-transform duration-300 ${
                pulseHeart ? "scale-110" : "scale-100"
              }`}
            >
              <Heart
                className={`w-6 h-6 ${
                  connected ? "text-rose-400" : "text-gray-500"
                }`}
              />
            </div>
            <h3 className="text-lg font-semibold text-white">
              Blood Pressure {connected ? "🟢" : "🔴"}
            </h3>
          </div>

          <div
            className={`flex items-center gap-1 text-sm ${
              isHealthy ? "text-green-400" : "text-red-400"
            }`}
          >
            <TrendingUp className="w-4 h-4" />
            <span>
              {isHealthy ? "Within healthy range" : "Check your BP!"}
            </span>
          </div>
        </div>

        <div className="flex items-baseline gap-3 mb-3">
          <div className="text-5xl font-bold text-white group-hover:text-rose-300">
            {bpData.bp_systolic}
          </div>

          <div className="text-3xl text-rose-300">/</div>

          <div className="text-5xl font-bold text-white group-hover:text-rose-300">
            {bpData.bp_diastolic}
          </div>

          <div className="text-rose-300 text-lg">mmHg</div>
        </div>
      </div>
    </div>
  );
}

export default React.memo(BloodPressureCard);

    
