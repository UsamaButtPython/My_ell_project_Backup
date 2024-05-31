import React from 'react'
import {Navigate } from "react-router-dom";
export const Logout = () => {
    function Empty_local_storage() {
        window.localStorage.clear();
        // window.localStorage.removeItem("isAuthenticated");
        // window.localStorage.removeItem("user_data");
        return <Navigate to='/login'  />  
    }
    return (
        <Empty_local_storage/>
    )
}

export default Logout