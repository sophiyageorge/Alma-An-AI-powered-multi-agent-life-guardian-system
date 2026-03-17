import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authenticateUser } from "../../services/api";
import toast from 'react-hot-toast';


const AuthModel = ({ isOpen, onClose, setIsAuthenticated }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [gender, setGender] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState("signin");
  const navigate = useNavigate()
  const [loading,setLoading] = useState(false)

  if (!isOpen) return null;


  const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true)

  try {
    const { response, data } = await authenticateUser(mode, {
      name,
      email,
      dateOfBirth,
      gender,
      password,
    });

    if (!response.ok) {
      // alert(JSON.stringify(data, null, 2));
      if (!response.ok) {
  const errorData = await response.json();
  console.error("API Error:", errorData);
  toast.error(`Error: ${response.status}`);
  return;
}


      return;
    }

    if (mode === "signin") {
      localStorage.setItem("token", data.access_token);
      setIsAuthenticated(true);
      onClose();
      // alert("Authentication successful!");
      toast.success('Authentication successful!!')
     
      navigate("/home");
    } else {
      // alert("Registration successful! Please sign in.");
       toast.success('Registration successful! Please sign in.')
      setMode("signin");
    }
  } catch (error) {
    console.error("Auth error:", error);
  }
finally{
   setLoading(false)
}
};

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg w-96 text-black">
        <h2 className="text-xl font-bold mb-4">
          {mode === "signin" ? "Sign In" : "Sign Up"}
        </h2>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="Email"
            className="border p-2 rounded"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
            {mode === "signup" && (
    
      <><input
              type="text"
              placeholder="Full Name"
              className="border p-2 rounded"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required /><input
                type="date"
                className="border p-2 rounded"
                value={dateOfBirth}
                onChange={(e) => setDateOfBirth(e.target.value)}
                required /><select
                  className="border p-2 rounded"
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  required
                >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select></>

            )}
         
          <input
            type="password"
            placeholder="Password"
            className="border p-2 rounded"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

        <button
  className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 flex items-center justify-center"
  disabled={loading} // optionally disable while loading
>
  {loading ? (
    <>
      <svg
        className="animate-spin h-5 w-5 mr-2 text-white"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
        />
      </svg>
      Loading...
    </>
  ) : (
    mode === "signin" ? "Login" : "Create Account"
  )}
</button>

                  <div className="mt-4 text-center text-sm">
  {mode === "signin" ? (
    <>
      Don’t have an account?{" "}
      <button
        type="button"
        className="text-blue-600 hover:underline"
        onClick={() => setMode("signup")}
      >
        Sign Up
      </button>
    </>
  ) : (
    <>
      Already have an account?{" "}
      <button
        type="button"
        className="text-blue-600 hover:underline"
        onClick={() => setMode("signin")}
      >
        Sign In
      </button>
    </>
  )}
</div>
        </form>

        <button
          onClick={onClose}
          className="mt-4 text-sm text-gray-500 hover:text-gray-700"
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default AuthModel;
