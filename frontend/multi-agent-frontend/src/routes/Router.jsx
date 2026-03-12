import { BrowserRouter } from "react-router-dom";
import { Routes } from "react-router-dom"; 
import { Route } from "react-router-dom";
import LandingPage from "../LandingPage";
import Home from "../Home";
import ProtectedRouter from "../ProtectedRouter";

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} /> 
        <Route element={<ProtectedRouter />}>
          <Route path="/home" element={<Home />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
 
