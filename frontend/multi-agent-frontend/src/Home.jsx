import { useState, useEffect } from "react";
import {
  Sparkles,
  Heart,
  Activity,
  TrendingUp,
  Apple,
  Flame,
  Droplets,
  Footprints,
  Calendar,
  Brain,
  Moon,
  Zap,
  Award,
  Target,
} from "lucide-react";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import image1 from "./assets/photo1.jpeg";
import image2 from "./assets/photo2.jpeg";
import image3 from "./assets/photo3.jpeg";
import image4 from "./assets/photo4.jpeg";
import image5 from "./assets/photo5.jpeg";
import image6 from "./assets/photo6.jpeg";
import AuthModel from "./components/auth/AuthModel";
import MealPlan from "./components/dashboard/MealPlan";
import BloodPressureCard from "./components/dashboard/BloodPressureCard";
import HeartRateCard from "./components/dashboard/HeartRateCard";
import AudioRecorder from "./components/dashboard/AudioRecorder";
import HeartRateChart from "./components/charts/HeartRateChart";
import BloodPressureChart from "./components/charts/BloodPressureChart";
import CurrentMeal from "./components/dashboard/CurrentMeal";
import Journal from "./components/dashboard/Journal";
import ExercisePlan from "./components/dashboard/ExercisePlan";
import HealthDailyUpdateForm from "./components/dashboard/HealthDailyUpdateForm";
// import MealPlanActions from "./UpdateMealPlan";






// const [mealPlan, setMealPlan] = useState(null);

function App() {
  const [mounted, setMounted] = useState(false);
  const [selectedMeal, setSelectedMeal] = useState(null);
  const [pulseHeart, setPulseHeart] = useState(false);
  const [currentBgIndex, setCurrentBgIndex] = useState(0);
  const [transcript, setTranscript] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  

  // Health and wellness themed background images from local assets
  const backgroundImages = [
    image1, // Yoga/Fitness
    image2, // Healthy Food
    image3, // Running/Exercise
    image4, // Nature/Wellness
    image5, // Meditation
    image6, // Healthy Lifestyle
  ];

  // Authentication

  // const [isAuthOpen, setIsAuthOpen] = useState(false);
  // const [authMode, setAuthMode] = useState("signin");
  // const [isAuthenticated, setIsAuthenticated] = useState(
  //   !!localStorage.getItem("token")
  // );

  //  const logout = () => {
  //   localStorage.removeItem("token");
  //   setIsAuthenticated(false);
  // };

  //  return (
  //   <div className="text-white min-h-screen bg-gray-900 p-6">
  //     <div className="flex justify-end gap-4">
  //       {isAuthenticated ? (
  //         <button
  //           onClick={logout}
  //           className="bg-red-600 px-4 py-2 rounded"
  //         >
  //           Logout
  //         </button>
  //       ) : (
  //         <>
  //           <button
  //             onClick={() => {
  //               setAuthMode("signin");
  //               setIsAuthOpen(true);
  //             }}
  //             className="bg-blue-600 px-4 py-2 rounded"
  //           >
  //             Sign In
  //           </button>

  //           <button
  //             onClick={() => {
  //               setAuthMode("signup");
  //               setIsAuthOpen(true);
  //             }}
  //             className="bg-green-600 px-4 py-2 rounded"
  //           >
  //             Sign Up
  //           </button>
  //         </>
  //       )}
  //     </div>

  //     <AuthModal
  //       isOpen={isAuthOpen}
  //       onClose={() => setIsAuthOpen(false)}
  //       mode={authMode}
  //       setIsAuthenticated={setIsAuthenticated}
  //     />
  //   </div>
  // );


  useEffect(() => {
    setMounted(true);

    // Heart pulse animation
    const heartInterval = setInterval(() => {
      setPulseHeart(true);
      setTimeout(() => setPulseHeart(false), 1000);
    }, 2000);

    // Background slideshow - changes every 8 seconds
    const bgInterval = setInterval(() => {
      setCurrentBgIndex((prev) => (prev + 1) % backgroundImages.length);
    }, 8000);

    return () => {
      clearInterval(heartInterval);
      clearInterval(bgInterval);
    };
  }, [backgroundImages.length]);

  const meals = [
    {
      name: "Oatmeal with Berries",
      time: "7:30 AM",
      calories: 320,
      icon: "🥣",
      macros: { protein: 12, carbs: 54, fats: 8 },
    },
    {
      name: "Grilled Chicken Salad",
      time: "12:30 PM",
      calories: 450,
      icon: "🥗",
      macros: { protein: 35, carbs: 28, fats: 18 },
    },
    {
      name: "Salmon with Vegetables",
      time: "7:00 PM",
      calories: 580,
      icon: "🐟",
      macros: { protein: 42, carbs: 35, fats: 24 },
    },
  ];

  const heartRateData = [
    { time: "6 AM", rate: 62 },
    { time: "9 AM", rate: 75 },
    { time: "12 PM", rate: 88 },
    { time: "3 PM", rate: 82 },
    { time: "6 PM", rate: 95 },
    { time: "9 PM", rate: 70 },
    { time: "12 AM", rate: 65 },
  ];

  const stepData = [
    { day: "Mon", steps: 8200 },
    { day: "Tue", steps: 9400 },
    { day: "Wed", steps: 7800 },
    { day: "Thu", steps: 10200 },
    { day: "Fri", steps: 9100 },
    { day: "Sat", steps: 11500 },
    { day: "Sun", steps: 8650 },
  ];

  const calorieBreakdown = [
    { name: "Consumed", value: 1350, fill: "#f59e0b" },
    { name: "Remaining", value: 650, fill: "rgba(255,255,255,0.1)" },
  ];

  const bloodPressureHistory = [
    { day: "Mon", systolic: 120, diastolic: 78 },
    { day: "Tue", systolic: 118, diastolic: 76 },
    { day: "Wed", systolic: 122, diastolic: 79 },
    { day: "Thu", systolic: 119, diastolic: 77 },
    { day: "Fri", systolic: 118, diastolic: 76 },
    { day: "Sat", systolic: 116, diastolic: 74 },
    { day: "Sun", systolic: 118, diastolic: 76 },
  ];

  const weeklyActivities = [
    {
      day: "Mon",
      workouts: ["Cardio", "Hydration"],
      color: "from-orange-400 to-orange-600",
    },
    {
      day: "Tue",
      workouts: ["Meditation", "Strength"],
      color: "from-violet-400 to-violet-600",
    },
    {
      day: "Wed",
      workouts: ["Yoga", "Hydration"],
      color: "from-emerald-400 to-emerald-600",
    },
    {
      day: "Thu",
      workouts: ["HIIT", "Sleep"],
      color: "from-orange-400 to-orange-600",
    },
    {
      day: "Fri",
      workouts: ["Mindfulness", "Recovery"],
      color: "from-violet-400 to-violet-600",
    },
    {
      day: "Sat",
      workouts: ["Outdoor", "Hydration"],
      color: "from-emerald-400 to-emerald-600",
    },
    {
      day: "Sun",
      workouts: ["Rest", "Reflection"],
      color: "from-blue-400 to-blue-600",
    },
  ];

  return (
    
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 overflow-x-hidden relative">

      {/* Animated Slideshow Background with Local Images */}
      <div className="fixed inset-0 overflow-hidden">
        {backgroundImages.map((image, index) => (
          <div
            key={index}
            className={`absolute inset-0 transition-opacity duration-[2000ms] ease-in-out ${index === currentBgIndex ? "opacity-100" : "opacity-0"
              }`}
            style={{
              backgroundImage: `url(${image})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundRepeat: "no-repeat",
            }}
          >
            {/* Dark overlay for readability with subtle animation */}
            <div className="absolute inset-0 bg-gradient-to-br from-slate-900/95 via-blue-900/90 to-slate-900/95 transition-all duration-1000"></div>
          </div>
        ))}
      </div>

      {/* Animated Pattern overlay */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PHBhdGggZD0iTTM2IDE2YzAtMi4yMSAxLjc5LTQgNC00czQgMS43OSA0IDQtMS43OSA0LTQgNC00LTEuNzktNC00ek0yMCA0OGMwLTIuMjEgMS43OS00IDQtNHM0IDEuNzkgNCA0LTEuNzkgNC00IDQtNC0xLjc5LTQtNHoiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-20"></div>
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-rose-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: "1s" }}></div>
      </div>

      {/* Interactive Slideshow Progress Indicator */}
  
      <div className="fixed top-4 right-4 z-50 flex gap-2 bg-black/20 backdrop-blur-md rounded-full px-3 py-2">
        {backgroundImages.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentBgIndex(index)}
            className={`h-1.5 rounded-full transition-all duration-500 hover:scale-110 focus:outline-none ${index === currentBgIndex
                ? "w-8 bg-cyan-400 shadow-lg shadow-cyan-400/50"
                : "w-1.5 bg-white/30 hover:bg-white/50"
              }`}
            aria-label={`Go to slide ${index + 1}`}
          ></button>
        ))}
      </div>
    
{isAuthenticated && <p>Welcome, you are logged in!</p>}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header with Fade In Animation */}
        <header
          className={`mb-12 pt-6 transition-all duration-1000 ${mounted
              ? "opacity-100 translate-y-0"
              : "opacity-0 -translate-y-10"
            }`}
        >
          <div className="flex flex-wrap items-center gap-3 mb-2">
            <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl shadow-lg shadow-cyan-500/30 animate-bounce">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-3xl sm:text-4xl font-bold text-white bg-clip-text">
              Welcome !
            </h1>
          </div>
          <p className="text-cyan-200 text-base sm:text-lg ml-0 sm:ml-14">
            Your personalized wellness journey continues ✨
          </p>
        </header>

        {/* Stats Cards - Slide in from sides */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 mb-6">

          {/* Heart Rate card */}
               <HealthDailyUpdateForm /> 
           <HeartRateCard /> 
           {/* <HealthDailyUpdateForm /> */}
           

            {/* Blood Pressure Card */}

           <BloodPressureCard /> 
        
        
    
        </div>

        {/* Charts Section */}
        <div
          className={`grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6 transition-all duration-1000 ${mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
            }`}
          style={{ transitionDelay: "400ms" }}
        >
          {/* Heart Rate Chart */}

           {/* <HeartRateChart /> */}

          {/* Blood Pressure Chart */}

         {/* <BloodPressureChart /> */}
       
        </div>

        {/* Meal Plan Section */}
        <div
          className={`relative overflow-hidden bg-gradient-to-br from-amber-500/10 to-orange-500/10 backdrop-blur-xl border border-amber-500/20 rounded-2xl p-6 mb-6 hover:border-amber-500/40 transition-all duration-500 ${mounted ? "opacity-100 scale-100" : "opacity-0 scale-95"
            }`}
          style={{ transitionDelay: "500ms" }}
        >
          <div className="absolute top-0 left-0 w-40 h-40 bg-amber-500/10 rounded-full -ml-20 -mt-20 animate-pulse"></div>
        {/* <CurrentMeal /> */}
         <CurrentMeal />
        </div>
      

        {/* Weekly Meal Plan Section */}
        <div
          className={`relative overflow-hidden bg-gradient-to-br from-amber-500/10 to-orange-500/10 backdrop-blur-xl border border-amber-500/20 rounded-2xl p-6 mb-6 hover:border-amber-500/40 transition-all duration-500 ${mounted ? "opacity-100 scale-100" : "opacity-0 scale-95"
            }`}
          style={{ transitionDelay: "500ms" }}
        >
          <div className="absolute top-0 left-0 w-40 h-40 bg-amber-500/10 rounded-full -ml-20 -mt-20 animate-pulse"></div>
                 
<MealPlan />

        </div>


        {/* Steps and Calories Section */}
     

        {/* Daily Exercise Plan */}
        <ExercisePlan />
        
{/* <AudioRecorder /> */}
 <div style={{ padding: "20px" }}>
   

      {/* Audio recorder component */}
      <AudioRecorder onTranscription={setTranscript} />
      {/* <AudioRecorder onTranscription={(text) => setTranscript(text)} /> */}

      {/* Display transcript */}
      {transcript && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            border: "1px solid #ccc",
            borderRadius: "8px",
            backgroundColor: "#f9f9f9",
          }}
        >
          <strong>Transcribed Text:</strong>
          <p style={{ marginTop: "10px", fontSize: "16px" }}>{ setTranscript(data.text)}</p>
         
        </div>
      )}
    </div>
      </div>
      {/* <Journal /> */}

      {/* <div>
    {mealPlan ? (
      <div>
        <h2>Meal Plan for Week {mealPlan.week}</h2>
        <pre>{mealPlan.meal_plan}</pre>
        <p>Approved: {mealPlan.approved ? "Yes ✅" : "No ❌"}</p>
      </div>
    ) : (
      <p>Loading meal plan...</p>
    )}
      
  </div> */}
{/* <div className="text-white min-h-screen bg-gray-900 p-6">
      <div className="flex justify-end gap-4">
        {isAuthenticated ? (
          <button
            onClick={logout}
            className="bg-red-600 px-4 py-2 rounded"
          >
            Logout
          </button>
        ) : (
          <>
            <button
              onClick={() => {
                setAuthMode("signin");
                setIsAuthOpen(true);
              }}
              className="bg-blue-600 px-4 py-2 rounded"
            >
              Sign In
            </button>

            <button
              onClick={() => {
                setAuthMode("signup");
                setIsAuthOpen(true);
              }}
              className="bg-green-600 px-4 py-2 rounded"
            >
              Sign Up
            </button>
          </>
        )}
      </div>

      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        mode={authMode}
        setIsAuthenticated={setIsAuthenticated}
      />
    </div> */}
  
      {/* Add custom animations */}
      <style>{`
        @keyframes progress {
          from {
            width: 0%;
          }
          to {
            width: 80%;
          }
        }
        
        @keyframes drawCircle {
          from {
            stroke-dasharray: 0 471;
          }
          to {
            stroke-dasharray: ${(8650 / 10000) * 471} 471;
          }
        }
        
        @keyframes shimmer {
          0% {
            transform: translateX(-200%);
          }
          100% {
            transform: translateX(200%);
          }
        }
        
        .animate-shimmer {
          animation: shimmer 3s infinite;
        }
      `}</style>
    </div>

    
  );

  //  return (
  //   <div>
  //     <h1>My App</h1>

  //     <MealPlan />   {/* ✅ Component added here */}

  //   </div>
  // );
}

export default App;
