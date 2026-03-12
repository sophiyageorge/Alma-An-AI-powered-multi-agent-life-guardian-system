// import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
// import { Heart } from "lucide-react";

// function BloodPressureChart() {
//   const bloodPressureHistory = [
//     { day: "Mon", systolic: 120, diastolic: 80 },   
//     { day: "Tue", systolic: 125, diastolic: 82 },
//     { day: "Wed", systolic: 118, diastolic: 78 },
//     { day: "Thu", systolic: 122, diastolic: 81 },   
//     { day: "Fri", systolic: 119, diastolic: 79 },
//     { day: "Sat", systolic: 121, diastolic: 80 },
//   ];
// return(
// <div className="relative overflow-hidden bg-gradient-to-br from-rose-500/10 to-pink-500/10 backdrop-blur-xl border border-rose-500/20 rounded-2xl p-6 hover:border-rose-500/40 hover:shadow-2xl hover:shadow-rose-500/10 transition-all duration-500">
//             <div className="absolute top-0 right-0 w-32 h-32 bg-rose-500/10 rounded-full -mr-16 -mt-16 animate-pulse"></div>
//             <div className="relative">
//               <div className="flex items-center justify-between mb-4">
//                 <h3 className="text-lg font-bold text-white">
//                   Blood Pressure History
//                 </h3>
//                 <Heart className="w-5 h-5 text-rose-400 animate-pulse" />
//               </div>
//               <ResponsiveContainer width="100%" height={250}>
//                 <AreaChart data={bloodPressureHistory}>
//                   <CartesianGrid
//                     strokeDasharray="3 3"
//                     stroke="rgba(255,255,255,0.1)"
//                   />
//                   <XAxis
//                     dataKey="day"
//                     stroke="rgba(255,255,255,0.5)"
//                     style={{ fontSize: "12px" }}
//                   />
//                   <YAxis
//                     stroke="rgba(255,255,255,0.5)"
//                     style={{ fontSize: "12px" }}
//                     domain={[70, 130]}
//                   />
//                   <Tooltip
//                     contentStyle={{
//                       backgroundColor: "rgba(15,23,42,0.95)",
//                       border: "1px solid rgba(244,63,94,0.3)",
//                       borderRadius: "12px",
//                       color: "#fff",
//                       backdropFilter: "blur(10px)",
//                     }}
//                   />
//                   <Area
//                     type="monotone"
//                     dataKey="systolic"
//                     stroke="#f43f5e"
//                     fill="#f43f5e"
//                     fillOpacity={0.3}
//                     animationDuration={2000}
//                   />
//                   <Area
//                     type="monotone"
//                     dataKey="diastolic"
//                     stroke="#fb7185"
//                     fill="#fb7185"
//                     fillOpacity={0.2}
//                     animationDuration={2000}
//                   />
//                 </AreaChart>
//               </ResponsiveContainer>
//               <div className="mt-4 flex gap-4 text-sm justify-center p-3 bg-white/5 rounded-lg">
//                 <div className="flex items-center gap-2">
//                   <span className="w-3 h-3 bg-rose-400 rounded-full"></span>
//                   <span className="text-gray-300">Systolic</span>
//                 </div>
//                 <div className="flex items-center gap-2">
//                   <span className="w-3 h-3 bg-pink-400 rounded-full"></span>
//                   <span className="text-gray-300">Diastolic</span>
//                 </div>
//               </div>
//             </div>
//           </div>
// );

// }

// export default BloodPressureChart;



// import React,{ useState, useEffect } from "react";
// import { Heart, TrendingUp } from "lucide-react";





// function BloodPressureCard() {
//   const [bpData, setBpData] = useState({ bp_systolic: 0, bp_diastolic: 0 });
//   const [pulseHeart, setPulseHeart] = useState(false);
//   const [mounted, setMounted] = useState(false);
  
//  useEffect(() => {
//   const fetchData = async () => {
//     try {
//       const res = await fetch("http://localhost:8000/realtime/health/normal");
//       const data = await res.json();
//       setBpData(data[0]);
//     } catch (error) {
//       console.error("Error fetching BP data:", error);
//     }
//   };


//   fetchData();
// }, []);


//  console.log("BloodPressureCard data:", bpData)


//     useEffect(() => {
//     setMounted(true);

//   },[]);


// //  an

//   return (

//       <div
//             className={`group relative overflow-hidden bg-gradient-to-br from-rose-500/10 to-pink-500/10 backdrop-blur-xl border border-rose-500/20 rounded-2xl p-6 hover:border-rose-500/40 hover:shadow-2xl hover:shadow-rose-500/20 transition-all duration-500 hover:scale-[1.02] ${mounted
//                 ? "opacity-100 translate-x-0"
//                 : "opacity-0 -translate-x-20"
//               }`}
//             style={{ transitionDelay: "200ms" }}
//           >
//             <div className="absolute top-0 right-0 w-32 h-32 bg-rose-500/10 rounded-full -mr-16 -mt-16 group-hover:scale-150 transition-transform duration-500"></div>
//             <div className="absolute inset-0 bg-gradient-to-r from-transparent via-rose-500/5 to-transparent translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000"></div>

//             <div className="relative">
//               <div className="flex items-center justify-between mb-4">
//                 <div className="flex items-center gap-3">
//                   <div
//                     className={`p-3 bg-rose-500/20 rounded-xl transition-transform duration-300 scale-110
//                       `}
//                   >
//                     <Heart className="w-6 h-6 text-rose-400" />
//                   </div>
//                   <h3 className="text-lg font-semibold text-white">
//                     Blood Pressure
//                   </h3>
//                 </div>
//                 <div className="flex items-center gap-1 text-green-400 text-sm animate-pulse">
//                   <TrendingUp className="w-4 h-4" />
//                   <span className="text-sm text-gray-300">
//                       {bpData.bp_systolic < 120 && bpData.bp_diastolic < 80
//                         ? "Within healthy range"
//                         : "Check your BP!"}
//                   </span>
//                 </div>
//               </div>

//               <div className="flex items-baseline gap-3 mb-3">
//                 <div className="text-5xl font-bold text-white transition-all duration-300 group-hover:text-rose-300">
//                  {bpData.bp_systolic}
//                 </div>
//                 <div className="text-3xl text-rose-300">/</div>
//                 <div className="text-5xl font-bold text-white transition-all duration-300 group-hover:text-rose-300">
//                   {bpData.bp_diastolic}
//                 </div>
//                 <div className="text-rose-300 text-lg">mmHg</div>
//               </div>

//               <div className="flex items-center gap-2">
//                 <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
//                   <div className="h-full bg-gradient-to-r from-green-400 to-emerald-500 rounded-full animate-[progress_2s_ease-out]" style={{ width: "80%" }}></div>
//                 </div>
//                 <span className="text-sm text-gray-300">
//                   Within healthy range
//                 </span>
//               </div>
//             </div>
//           </div>
//   );

// }


// export default React.memo(BloodPressureCard);


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

    
