// import React,{ useState, useEffect } from "react";
// import { Heart, TrendingUp } from "lucide-react"; 

// function BloodPressureCard() {
//   const [bpData, setBpData] = useState({ bp_systolic: 0, bp_diastolic: 0 });
//   const [pulseHeart, setPulseHeart] = useState(false);
//   const [mounted, setMounted] = useState(false);  

//     useEffect(() => {
//     setMounted(true);
//   }, []);

//   return (

  
//   <div
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
//                     className={`p-3 bg-rose-500/20 rounded-xl transition-transform duration-300 ${pulseHeart ? "scale-110" : "scale-100"
//                       }`}
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
//                       {/* {bpData.bp_systolic < 120 && bpData.bp_diastolic < 80
//                         ? "Within healthy range"
//                         : "Check your BP!"} */}
//                         Within healthy range
//                   </span>
//                 </div>
//               </div>

//               <div className="flex items-baseline gap-3 mb-3">
//                 <div className="text-5xl font-bold text-white transition-all duration-300 group-hover:text-rose-300">
//                  {/* {bpData.bp_systolic} */}
//                  120
//                 </div>
//                 <div className="text-3xl text-rose-300">/</div>
//                 <div className="text-5xl font-bold text-white transition-all duration-300 group-hover:text-rose-300">
//                   {/* {bpData.bp_diastolic} */}
//                   80
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
// import React, { useState, useEffect } from "react";
// import { Heart, TrendingUp } from "lucide-react";

// function BloodPressureCard() {
//   const [bpData, setBpData] = useState({ bp_systolic: 0, bp_diastolic: 0 });
//   const [pulseHeart, setPulseHeart] = useState(false);
//   const [mounted, setMounted] = useState(false);

//   useEffect(() => {
//     setMounted(true);

//     const ws = new WebSocket("ws://localhost:8000/realtime/ws");
//      ws.onopen = () => {
//     console.log("WebSocket connected");
//     // Now it's safe to send
//     ws.send(JSON.stringify({ type: "hello", msg: "Client connected!" }));
//   };

//     ws.onmessage = (event) => {
//       const msg = JSON.parse(event.data);

//        if (msg.bp_systolic && msg.bp_diastolic) {
//     setBpData({
//       bp_systolic: msg.bp_systolic,
//       bp_diastolic: msg.bp_diastolic,
//     });

//     setPulseHeart(true);
//     setTimeout(() => setPulseHeart(false), 300);
//   }

//     };

//     return () => ws.close();
//   });

//   const isHealthy =
//     bpData.bp_systolic < 120 && bpData.bp_diastolic < 80;

//   return (
//     <div
//       className={`group relative overflow-hidden bg-gradient-to-br 
//       from-rose-500/10 to-pink-500/10 backdrop-blur-xl 
//       border border-rose-500/20 rounded-2xl p-6 
//       hover:border-rose-500/40 hover:shadow-2xl 
//       hover:shadow-rose-500/20 transition-all duration-500 
//       hover:scale-[1.02] ${
//         mounted ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-20"
//       }`}
//       style={{ transitionDelay: "200ms" }}
//     >
//       <div className="relative">
//         <div className="flex items-center justify-between mb-4">
//           <div className="flex items-center gap-3">
//             <div
//               className={`p-3 bg-rose-500/20 rounded-xl transition-transform duration-300 ${
//                 pulseHeart ? "scale-110" : "scale-100"
//               }`}
//             >
//               <Heart className="w-6 h-6 text-rose-400" />
//             </div>
//             <h3 className="text-lg font-semibold text-white">
//               Blood Pressure
//             </h3>
//           </div>

//           <div
//             className={`flex items-center gap-1 text-sm ${
//               isHealthy ? "text-green-400" : "text-red-400"
//             }`}
//           >
//             <TrendingUp className="w-4 h-4" />
//             <span>
//               {isHealthy ? "Within healthy range" : "Check your BP!"}
//             </span>
//           </div>
//         </div>

//         <div className="flex items-baseline gap-3 mb-3">
//           <div className="text-5xl font-bold text-white group-hover:text-rose-300">
//             {bpData.bp_systolic}
//           </div>
//           <div className="text-3xl text-rose-300">/</div>
//           <div className="text-5xl font-bold text-white group-hover:text-rose-300">
//             {bpData.bp_diastolic}
//           </div>
//           <div className="text-rose-300 text-lg">mmHg</div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default React.memo(BloodPressureCard);

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


import React, { useState, useEffect, useRef } from "react";
import { Heart, TrendingUp } from "lucide-react";

function BloodPressureCard() {
  const [bpData, setBpData] = useState({
    bp_systolic: "--",
    bp_diastolic: "--",
  });

  const [pulseHeart, setPulseHeart] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [connected, setConnected] = useState(false);

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
      console.log("BP WebSocket connected");
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        if (msg.bp_systolic && msg.bp_diastolic) {
          setBpData({
            bp_systolic: msg.bp_systolic,
            bp_diastolic: msg.bp_diastolic,
          });

          // Trigger pulse animation
          setPulseHeart(true);
          setTimeout(() => setPulseHeart(false), 300);
        }
      } catch (err) {
        console.error("BP parse error:", err);
      }
    };

    ws.onclose = () => {
      console.log("BP WebSocket closed. Reconnecting...");
      setConnected(false);
      setTimeout(connectWebSocket, 2000); // auto reconnect
    };

    ws.onerror = (err) => {
      console.error("BP WebSocket error:", err);
      ws.close();
    };
  };

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

    
