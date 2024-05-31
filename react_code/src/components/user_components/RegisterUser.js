import React from 'react'
import  {Route, Navigate,useNavigate } from 'react-router-dom'

function RegisterUser() {
    const navigate=useNavigate()
    const reg = (e) =>{
        e.preventDefault();
        const email = e.target.email.value;
        const pass = e.target.pass.value;
        const username = e.target.username.value;
        // const value = e.target.value;
        console.log(pass,"me")
        eel.register(username,email,pass)().then((r) => {
          console.log(r.data);
          if (r.success==true){
            localStorage.setItem("user_data", JSON.stringify(r.data));
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
    <h1>Here you can Register</h1>
  
    <form id="RegForm" onSubmit={reg}>
        <input type="text" name="unamename" id="username" required/>
        <br/>
        <input type="email" name="email" id="email" required/>
        <br/>
        <input type="password" name="pass" id="pass" required/>
        <br/>
        <button type="submit"> Submit</button>
    </form>
</>
  )
}

export default RegisterUser