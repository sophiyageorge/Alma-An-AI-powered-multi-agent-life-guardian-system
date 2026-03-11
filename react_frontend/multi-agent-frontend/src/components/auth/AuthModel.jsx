import { useState } from "react";

const AuthModel = ({ isOpen, onClose, setIsAuthenticated }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [gender, setGender] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState("signin");

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();

    const endpoint =
      mode === "signin"
        ? "http://localhost:8000/users/login"
        : "http://localhost:8000/users/register";
        
        const body =
  mode === "signin"
    ? JSON.stringify({ email, password })
    : JSON.stringify({
          name,
          email,
          date_of_birth: dateOfBirth,
          gender,
          password,
        });

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: body,
        
      });

      const data = await response.json();

      console.log("Endpoint:", endpoint);
      console.log("Request body:", body);
      console.log("Response:", data);

      if (!response.ok) {
          console.log("Backend error:", data);
          alert(JSON.stringify(data, null, 2));
        }

      if (response.ok) {
        if (mode === "signin") {
        localStorage.setItem("token", data.access_token);
        setIsAuthenticated(true);
        onClose();
        alert("Authentication successful!");
      } else {
        alert("Registration successful! Please sign in.");
        setMode("signin");}
        
      } else {
        alert(data.detail || "Authentication failed");
      }
    } catch (error) {
      console.error("Auth error:", error);
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
          {/* <input
            type="text"
            placeholder="Name"
            className="border p-2 rounded"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input
            type="date"
            placeholder="Date of Birth"
            className="border p-2 rounded"
            value={dateOfBirth}
            onChange={(e) => setDateOfBirth(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Gender"
            className="border p-2 rounded"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            required
          /> */}
          <input
            type="password"
            placeholder="Password"
            className="border p-2 rounded"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
            {mode === "signin" ? "Login" : "Create Account"}
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
