import React from 'react'
const delete_func = (e) =>{
    e.preventDefault();
    const id = JSON.parse(localStorage.getItem("user_data")).id;

    // const value = e.target.value;
    eel.delete(id)().then((r) => {
      console.log(r);
      if (r.success==true){
        // localStorage.setItem("user_data",JSON.stringify(r.data));
        // localStorage.setItem("isAuthenticated",true);
        // localStorage.getItem("user_data");
        // return navigate('/')
        console.log(r)
      }
      else{
        alert(r.error_msg)
      }
  });
}
function DeleteUser() {
    function Delete_user() {
         
    }
  return (
    <div>Delete</div>
  )
}

export default DeleteUser