import { useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";

function LogoutButton() {
  const navigate = useNavigate();

  const handleLogout = () => {
    try {
      console.log("LogoutButton clicked");
      // remove stored authentication data
      localStorage.removeItem("token");
     

      // optional: clear all storage
      // localStorage.clear();

      // redirect to login page
      navigate("/");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <button className="group flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-400/30
    bg-white/5 text-cyan-300 text-sm font-medium backdrop-blur-sm
    hover:bg-cyan-500/10 hover:border-cyan-400/60 hover:text-white
    transition-all duration-300" onClick={handleLogout}>
      
    <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none"
      viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
      <path strokeLinecap="round" strokeLinejoin="round"
        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h6a2 2 0 012 2v1" />
    </svg>
    Sign out
  </button>
  );
}

export default LogoutButton;