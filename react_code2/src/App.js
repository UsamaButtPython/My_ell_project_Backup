import React, { useEffect } from "react";
import logo from "./logo.svg";
import "./App.css";

import { eel } from "./eel.js";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Navigate
} from "react-router-dom";

import Login from './components/user_components/Login';
import Home from './components/user_components/Home';
import RegisterUser from "./components/user_components/RegisterUser";
import Logout from "./components/user_components/Logout";
import DeleteUser from "./components/user_components/DeleteUser";
import UpdateUser from "./components/user_components/UpdateUser";

function App() {
 

  

  
  eel.set_host("ws://localhost:8888");
  eel.hello();
  // useEffect(() => {
  //   eel.set_host("ws://localhost:8888");
  //   eel.hello();
  // }, []);
  function RequireAuth({ children, redirectTo }) {
    let isAuthenticated = localStorage.getItem('isAuthenticated');
    return isAuthenticated ? children : <Navigate to={redirectTo} />;
  }
  return (
   <>

<Routes>
<Route default path="/login" element={  <Login />} />
{/* <Route path="*" element={  <Home />} /> */}
{/* <Route path="*" element={<Navigate to="/home" replace />} /> */}
<Route path="/register" element={  <RegisterUser />} />
<Route path="/logout" element={  <Logout />} />
<Route path="/delete" element={  <DeleteUser />} />
<Route path="/update" element={  <UpdateUser />} />

<Route path="*" element={ <RequireAuth redirectTo="/login">  <Home /> </RequireAuth> } />
</Routes>

<Link to="/">Home</Link>
<Link to="/login">Login</Link>
<Link to="/delete">Delete</Link>
<Link to="/update">Update</Link>
<Link to="/logout">Logout</Link>
<Link to="/register">Register</Link>



   </>
  )
}
export default App;
