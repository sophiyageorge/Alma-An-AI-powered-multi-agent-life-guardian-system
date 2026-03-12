import React from 'react'
import { getRecommendations } from "../../services/api";
import { useState, useEffect } from 'react';
import { Calendar, Sparkles, Activity, Zap, AlertTriangle, Heart, Flame } from "lucide-react";

function extractExerciseData(response) {
  try {
    const raw = response.llm_response;
    const jsonMatch = raw.match(/```json\s*([\s\S]*?)\s*```/);
    if (!jsonMatch) throw new Error("No JSON block found in llm_response");
    const parsed = JSON.parse(jsonMatch[1]);
    return {
      plan: parsed.plan || [],
      warnings: parsed.warnings || [],
      recovery_advice: parsed.recovery_advice || "",
      intensity: parsed.intensity || ""
    };
  } catch (error) {
    console.error("Error parsing exercise plan:", error);
    return { plan: [], warnings: [], recovery_advice: "", intensity: "" };
  }
}

const intensityConfig = {
  low: {
    label: "Low Intensity",
    color: "from-emerald-400 to-teal-500",
    bg: "bg-emerald-500/20",
    border: "border-emerald-500/30",
    text: "text-emerald-300",
    icon: <Activity className="w-3 h-3" />
  },
  moderate: {
    label: "Moderate Intensity",
    color: "from-amber-400 to-orange-500",
    bg: "bg-amber-500/20",
    border: "border-amber-500/30",
    text: "text-amber-300",
    icon: <Zap className="w-3 h-3" />
  },
  high: {
    label: "High Intensity",
    color: "from-red-400 to-rose-500",
    bg: "bg-red-500/20",
    border: "border-red-500/30",
    text: "text-red-300",
    icon: <Flame className="w-3 h-3" />
  }
};

const ExercisePlan = () => {
  const [exercise, setExercise] = useState({ plan: [], warnings: [], recovery_advice: "", intensity: "" });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getRecommendations();
        const extracted = extractExerciseData(data);
        console.log("Extracted Exercise Data:", extracted);
        setExercise(extracted);
      } catch (error) {
        console.error("Error fetching exercise recommendations:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const intensity = intensityConfig[exercise.intensity?.toLowerCase()] || intensityConfig.low;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-2 border-violet-500/30 border-t-violet-400 rounded-full animate-spin" />
          <span className="text-sm text-gray-400">Loading your plan...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-white/20 hover:shadow-2xl transition-all duration-500">
      
      {/* Header */}
      <div className="flex flex-wrap items-center gap-3 mb-6">
        <div className="p-2 bg-gradient-to-br from-violet-400 to-fuchsia-500 rounded-xl shadow-lg shadow-violet-500/30">
          <Calendar className="w-5 h-5 text-white" />
        </div>
        <h2 className="text-xl font-bold text-white">Your Exercise Plan</h2>
        <div className="ml-auto flex items-center gap-2">
          {/* Intensity Badge */}
          <div className={`flex items-center gap-1 px-3 py-1 ${intensity.bg} border ${intensity.border} rounded-full`}>
            <span className={`${intensity.text}`}>{intensity.icon}</span>
            <span className={`text-xs ${intensity.text} font-medium`}>{intensity.label}</span>
          </div>
          <div className="flex items-center gap-1 px-3 py-1 bg-violet-500/20 border border-violet-500/30 rounded-full">
            <Sparkles className="w-3 h-3 text-violet-400 animate-pulse" />
            <span className="text-xs text-violet-300">AI Curated</span>
          </div>
        </div>
      </div>

      {/* Exercise Plan Cards */}
      {exercise.plan.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {exercise.plan.map((item, idx) => (
            <div
              key={idx}
              className="group relative bg-gradient-to-br from-white/5 to-white/10 border border-white/10 rounded-xl p-4 hover:border-white/20 hover:scale-[1.02] hover:shadow-lg transition-all duration-300 cursor-pointer"
            >
              {/* Card gradient overlay on hover */}
              <div className="absolute inset-0 bg-gradient-to-br from-violet-500/10 to-fuchsia-500/10 opacity-0 group-hover:opacity-100 rounded-xl transition-opacity duration-300" />

              <div className="relative">
                {/* Exercise number badge */}
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-semibold text-violet-400 bg-violet-500/20 border border-violet-500/30 px-2 py-0.5 rounded-full">
                    Exercise {idx + 1}
                  </span>
                  {item.duration && (
                    <span className="text-xs text-gray-400 flex items-center gap-1">
                      <Zap className="w-3 h-3" /> {item.duration}
                    </span>
                  )}
                </div>

                {/* Exercise name */}
                <h3 className="text-base font-bold text-white mb-2 group-hover:text-violet-200 transition-colors duration-300">
                  {item.name || item.exercise || item.activity || `Exercise ${idx + 1}`}
                </h3>

                {/* Description / sets / reps / notes */}
                {item.description && (
                  <p className="text-xs text-gray-400 mb-2 leading-relaxed">{item.description}</p>
                )}
                {item.sets && (
                  <div className="flex gap-2 mt-2">
                    <span className="text-xs bg-white/5 text-gray-300 px-2 py-1 rounded-lg">
                      Sets: <span className="text-white font-medium">{item.sets}</span>
                    </span>
                    {item.reps && (
                      <span className="text-xs bg-white/5 text-gray-300 px-2 py-1 rounded-lg">
                        Reps: <span className="text-white font-medium">{item.reps}</span>
                      </span>
                    )}
                  </div>
                )}
                {item.notes && (
                  <p className="text-xs text-gray-500 mt-2 italic">{item.notes}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-10 text-gray-500">No exercise plan available.</div>
      )}

      {/* Warnings */}
      {exercise.warnings.length > 0 && (
        <div className="mb-4 p-4 bg-amber-500/10 border border-amber-500/20 rounded-xl">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span className="text-sm font-semibold text-amber-300">Heads Up</span>
          </div>
          <ul className="space-y-1">
            {exercise.warnings.map((w, i) => (
              <li key={i} className="text-xs text-amber-200/80 flex items-start gap-2">
                <span className="mt-1 w-1 h-1 rounded-full bg-amber-400 flex-shrink-0" />
                {w}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recovery Advice */}
      {exercise.recovery_advice && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
          <div className="flex items-center gap-2 mb-1">
            <Heart className="w-4 h-4 text-emerald-400" />
            <span className="text-sm font-semibold text-emerald-300">Recovery Advice</span>
          </div>
          <p className="text-xs text-emerald-200/80 leading-relaxed">{exercise.recovery_advice}</p>
        </div>
      )}
    </div>
  );
};

export default ExercisePlan;
// import React from 'react'
// import {getRecommendations} from "../../services/api";
// import { useState, useEffect } from 'react';
// import { Calendar, Sparkles, Activity, Zap, Droplets, Moon } from "lucide-react";

// function extractExerciseData(response) {
//   try {
//     const raw = response.llm_response;

//     // 1️⃣ Extract JSON block between ```json and ```
//     const jsonMatch = raw.match(/```json\s*([\s\S]*?)\s*```/);

//     if (!jsonMatch) {
//       throw new Error("No JSON block found in llm_response");
//     }

//     const jsonString = jsonMatch[1];

//     // 2️⃣ Parse JSON safely
//     const parsed = JSON.parse(jsonString);

//     // 3️⃣ Return structured data
//     return {
//       plan: parsed.plan || [],
//       warnings: parsed.warnings || [],
//       recovery_advice: parsed.recovery_advice || "",
//       intensity: parsed.intensity || ""
//     };

//   } catch (error) {
//     console.error("Error parsing exercise plan:", error);

//     return {
//       plan: [],
//       warnings: [],
//       recovery_advice: "",
//       intensity: ""
//     };
//   }
// }

// const ExercisePlan = () => {
//     const [exercise, setExercise] = useState([]);
//     useEffect(() => {
//         const fetchData = async () => {
//             try {   
//                 const data = await getRecommendations();
//                 const extracted = extractExerciseData(data);
//                 console.log("Extracted Exercise Data:", extracted);
//                 setExercise(extracted);
//             } catch (error) {
//                 console.error("Error fetching exercise recommendations:", error);
//             }
//         };
//         fetchData();
//     }, []);


//   return (
//     <div>
// {/*          
//  <div
//           className={`relative overflow-hidden bg-gradient-to-br from-white/5 to-white/10 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-white/20 hover:shadow-2xl transition-all duration-500 
//             }`}
//           style={{ transitionDelay: "800ms" }}
//         >
//           <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-200%] animate-shimmer"></div>

//           <div className="flex flex-wrap items-center gap-3 mb-6">
//             <div className="p-2 bg-gradient-to-br from-violet-400 to-fuchsia-500 rounded-xl hover:scale-110 transition-transform duration-300 shadow-lg shadow-violet-500/30">
//               <Calendar className="w-5 h-5 text-white" />
//             </div>
//             <h2 className="text-xl font-bold text-white">
//               Your Daily Exercise Plan
//             </h2>
//             <div className="ml-auto flex items-center gap-1 px-3 py-1 bg-violet-500/20 border border-violet-500/30 rounded-full hover:bg-violet-500/30 transition-colors duration-300">
//               <Sparkles className="w-3 h-3 text-violet-400 animate-pulse" />
//               <span className="text-xs text-violet-300">AI Curated</span>
//             </div>
//           </div>

//           <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-6">
//             {weeklyActivities.map((day, idx) => (
//               <div
//                 key={idx}
//                 className="group relative bg-gradient-to-br from-white/5 to-white/10 border border-white/10 rounded-xl p-3 sm:p-4 hover:border-white/20 hover:scale-105 hover:shadow-lg transition-all duration-300 cursor-pointer min-w-[100px]"
//                 style={{ transitionDelay: `${900 + idx * 50}ms` }}
//               >
//                 <div
//                   className={`absolute inset-0 bg-gradient-to-br ${day.color} opacity-0 group-hover:opacity-20 rounded-xl transition-opacity duration-300`}
//                 ></div>
//                 <div className="relative text-center">
//                   <div className="text-sm font-bold text-white mb-3 group-hover:scale-110 transition-transform duration-300">
//                     {day.day}
//                   </div>
//                   <div className="space-y-2">
//                     {day.workouts.map((workout, wIdx) => (
//                       <div
//                         key={wIdx}
//                         className="text-xs text-gray-300 bg-white/5 px-2 py-1 rounded-lg group-hover:bg-white/10 transition-colors duration-300"
//                       >
//                         {workout}
//                       </div>
//                     ))}
//                   </div>
//                 </div>
//               </div>
//             ))}
//           </div>

//           <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4 pt-4 border-t border-white/10">
//             {[
//               { value: "12", label: "Workouts", icon: <Activity className="w-4 h-4" /> },
//               { value: "5.5", label: "Active Hours", icon: <Zap className="w-4 h-4" /> },
//               { value: "18L", label: "Hydration Goal", icon: <Droplets className="w-4 h-4" /> },
//               { value: "56", label: "Sleep Hours", icon: <Moon className="w-4 h-4" /> },
//             ].map((stat, idx) => (
//               <div
//                 key={idx}
//                 className="text-center p-3 sm:p-4 rounded-lg bg-white/5 hover:bg-white/10 hover:scale-105 transition-all duration-300 group min-w-[80px]"
//                 style={{ transitionDelay: `${1000 + idx * 100}ms` }}
//               >
//                 <div className="flex items-center justify-center gap-2 mb-2">
//                   <div className="text-violet-400 group-hover:scale-110 transition-transform duration-300">
//                     {stat.icon}
//                   </div>
//                   <div className="text-2xl font-bold text-white group-hover:text-violet-300 transition-colors duration-300">
//                     {stat.value}
//                   </div>
//                 </div>
//                 <div className="text-xs text-gray-400">{stat.label}</div>
//               </div>
//             ))}
//           </div>
//         </div> */}
      
//     </div>
//   )
// }

// export default ExercisePlan


