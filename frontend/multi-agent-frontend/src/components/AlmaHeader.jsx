import { useState, useEffect } from "react";
import LogoutButton from "./auth/LogoutButton";

// Sparkles SVG Icon
const SparklesIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
    stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
    className="w-5 h-5 text-white">
    <path d="M12 3l1.88 5.76a1 1 0 00.95.69H21l-4.94 3.58a1 1 0 00-.36 1.12L17.56 20 12 16.18 6.44 20l1.86-5.85a1 1 0 00-.36-1.12L3 9.45h6.17a1 1 0 00.95-.69z" />
  </svg>
);

// Logout Button
// const LogoutButton = () => (
//   <button className="group flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-400/30
//     bg-white/5 text-cyan-300 text-sm font-medium backdrop-blur-sm
//     hover:bg-cyan-500/10 hover:border-cyan-400/60 hover:text-white
//     transition-all duration-300">
//     <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none"
//       viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
//       <path strokeLinecap="round" strokeLinejoin="round"
//         d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h6a2 2 0 012 2v1" />
//     </svg>
//     Sign out
//   </button>
// );

export default function AlmaHeader({ isAuthenticated = true, userName = "" }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setMounted(true), 80);
    return () => clearTimeout(t);
  }, []);

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=DM+Sans:wght@300;400;500&display=swap');

        .alma-font { font-family: 'Cormorant Garamond', serif; }
        .body-font { font-family: 'DM Sans', sans-serif; }

        .alma-logo-glow {
          filter: drop-shadow(0 0 18px rgba(34,211,238,0.55));
        }

        .header-divider {
          background: linear-gradient(90deg, transparent, rgba(34,211,238,0.5), rgba(59,130,246,0.4), transparent);
        }

        @keyframes pulse-soft {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.75; transform: scale(1.08); }
        }
        .pulse-soft { animation: pulse-soft 2.8s ease-in-out infinite; }

        @keyframes shimmer {
          0% { background-position: -200% center; }
          100% { background-position: 200% center; }
        }
        .shimmer-text {
          background: linear-gradient(90deg,
            #67e8f9 0%,
            #ffffff 40%,
            #67e8f9 60%,
            #93c5fd 100%
          );
          background-size: 200% auto;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          animation: shimmer 4s linear infinite;
        }

        @keyframes fadeSlideDown {
          from { opacity: 0; transform: translateY(-14px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        .fade-slide { animation: fadeSlideDown 0.8s cubic-bezier(.22,.68,0,1.2) both; }
        .fade-slide-delay-1 { animation-delay: 0.12s; }
        .fade-slide-delay-2 { animation-delay: 0.26s; }
        .fade-slide-delay-3 { animation-delay: 0.40s; }

        .tag-pill {
          background: linear-gradient(135deg, rgba(34,211,238,0.12), rgba(59,130,246,0.1));
          border: 1px solid rgba(34,211,238,0.25);
        }
      `}</style>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 body-font">

        {/* Authenticated notice (invisible, keeps logic) */}
        {isAuthenticated && (
          <span className="sr-only">You are logged in</span>
        )}

        <header className={`mb-12 pt-4 transition-all duration-1000 ${mounted ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-10"}`}>

          {/* ── Top bar: Brand left / Logout right ── */}
          <div className="flex items-center justify-between mb-8 fade-slide">

            {/* Brand mark */}
            <div className="flex items-center gap-3">
              {/* Icon badge */}
              <div className="relative pulse-soft alma-logo-glow">
                <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-cyan-400 via-sky-400 to-blue-600
                  flex items-center justify-center shadow-lg shadow-cyan-500/40">
                  <SparklesIcon />
                </div>
                {/* Outer ring */}
                <div className="absolute inset-0 rounded-2xl border border-cyan-300/30 scale-110 pointer-events-none" />
              </div>

              {/* Product name */}
              <div className="flex flex-col leading-none">
                <span className="alma-font text-4xl sm:text-5xl font-light tracking-widest shimmer-text select-none">
                  alma
                </span>
                <span className="text-[10px] uppercase tracking-[0.22em] text-cyan-400/60 font-medium mt-0.5 ml-0.5">
                  Wellness
                </span>
              </div>
            </div>

            {/* Logout */}
            <LogoutButton />
          </div>

          {/* ── Thin divider ── */}
          <div className="header-divider h-px w-full mb-7 fade-slide fade-slide-delay-1 rounded-full" />

          {/* ── Welcome copy ── */}
          <div className="fade-slide fade-slide-delay-2">
            <h1 className="text-2xl sm:text-3xl font-light text-white/90 tracking-wide mb-2">
              Welcome back{userName ? (
                <span className="font-semibold text-cyan-300">, {userName}</span>
              ) : null}
            </h1>

            <div className="flex flex-wrap items-center gap-3 mt-3 fade-slide fade-slide-delay-3">
              <p className="text-cyan-200/70 text-sm sm:text-base font-light tracking-wide">
                Your personalized wellness journey continues
              </p>
              {/* Decorative pill */}
              <span className="tag-pill text-[11px] font-medium text-cyan-300 px-3 py-1 rounded-full tracking-wider uppercase">
                Today
              </span>
            </div>
          </div>

        </header>
      </div>
    </>
  );
}