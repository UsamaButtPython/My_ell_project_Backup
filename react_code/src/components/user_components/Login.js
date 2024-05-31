import React, { useState, useEffect } from 'react'
// import { useLocation, Navigate } from "react-router-dom";
import  {Route, Navigate,useNavigate } from 'react-router-dom'
const Login = () => {
  const navigate=useNavigate()
  console.log("in login")
  // const py_video_stop = () =>{
  //   // $( "#bg" ).replaceWith( '<img id="bg" src="" alt="">' );
  //   console.log("Off camera")
  //   eel.video_stop()()
  // }
  // useEffect(() => {
  //   // Update the document title using the browser API
  //   // document.title = `You clicked ${count} times`;
  //   py_video_stop()
  // });
  const login_func = (e) =>{
    e.preventDefault();
    const username = e.target.username.value;
    const pass = e.target.pass.value;

    // const value = e.target.value;
    var user_obj={"username":username,"password":pass}
    eel.login(user_obj)().then((r) => {
      console.log(r);
      if (r.success==true){
        localStorage.setItem("user_data",JSON.stringify(r.data));
        localStorage.setItem("isAuthenticated",true);
        localStorage.getItem("user_data");
        return navigate('/')
      }
      else{
        alert(r.error_msg)
      }
  });
}
  return (
    <>
    <h1>Here you can login</h1>
  
    <form id="loginForm" onSubmit={login_func}>
        <input type="text" name="username" id="username" required/>
        <br/>
        <input type="password" name="pass" id="pass" required/>
        <br/>
        <button type="submit"> Submit</button>
    </form>
</>
  )
}

export default Login