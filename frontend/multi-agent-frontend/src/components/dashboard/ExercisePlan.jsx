import React from 'react'
import { getRecommendations } from "../../services/api";
import { useState, useEffect } from 'react';
import { Calendar, Sparkles, Activity, Zap, AlertTriangle, Heart, Flame } from "lucide-react";

function extractExerciseData(response) {
  try {
    const raw = response.llm_response;

    // parse JSON string directly
    const parsed = typeof raw === "string" ? JSON.parse(raw) : raw;

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
      {/* Exercise Plan Cards */}
{exercise.plan.length > 0 ? (
   
        <div className="mb-6 p-6 bg-amber-500/10 border border-amber-500/30 rounded-2xl shadow-sm">
  {/* Header */}
  <h3 className="text-sm font-semibold text-amber-400 uppercase mb-3 tracking-wide">
    Recommendations
  </h3>

  {/* Exercise Plan */}
  <div className="text-gray-100 leading-relaxed space-y-2">
    {exercise.plan.map((item, idx) => (
      <p key={idx} className="text-sm">
        {item}
      </p>
    ))}
  </div>
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




