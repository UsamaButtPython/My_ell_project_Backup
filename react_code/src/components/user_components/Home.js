import React, { useState, useEffect } from 'react'
import { useNavigate } from "react-router-dom";
const Home = () => {
  const [start, setStart] = useState(false);
  const [disable_click, setDisableClick] = useState(false);


  function addRow() {
    const div = document.createElement('div');
  
    div.className = 'row';
  
    div.innerHTML = `
    <img id="bg2" style="width:25%" onerror="this.onerror=null; this.src='http://127.0.0.1:8001/stream_not_found'" src="http://127.0.0.1:8001" alt=""/>\
    <img id="bg2" style="width:25%" onerror="this.onerror=null; this.src='http://127.0.0.1:8002/stream_not_found'" src="http://127.0.0.1:8002" alt=""/>\
    <img id="bg3" style="width:25%" onerror="this.onerror=null; this.src='http://127.0.0.1:8003/stream_not_found'" src="http://127.0.0.1:8003" alt=""/>\
    <img id="bg4" style="width:25%" onerror="this.onerror=null; this.src='http://127.0.0.1:8004/stream_not_found'" src="http://127.0.0.1:8004" alt=""/>\
    `;
  
    document.getElementById('content').appendChild(div);
  }
 
  function removeRow() {
    const list = document.getElementById("content");
    list.removeChild(list.firstElementChild);
    // document.getElementById('content').removeChild(img.parentNode);
  }


  const py_video = (id) =>{
    eel.video_feed(id)().then(retData => {
        // close()
        console.log(retData);
        addRow()
        // setStart(retData);
        setDisableClick(false)

    }).catch(e => console.log(e));
 }

  const py_video_stop = () =>{
    eel.video_stop()().then(retData => {
      setStart(false);
      removeRow()
      setDisableClick(false)
  })
  .catch(e => console.log(e));   
  }

      
  function py_login(data) {
  eel.login(data)()
  }

  const shoot  = e => {
    const el = e.target
    if (el.className == "Start"){ 
      el.id
      console.log("el.currentTarget.id",el.id)
      py_video_stop();
      setDisableClick(true)
      py_video(el.id)
    }
    else{
      setDisableClick(true)
      py_video_stop();
    }
    console.log(el.className)
  }
  let user=null
  try {
    user= JSON.parse(localStorage.getItem("user_data")).username 
    } 
    catch (e) {
    user= null 
    }

  // console.log(JSON.parse(localStorage.getItem("user_data")).username) 
  return (
    <>
    <h1>Video Streaming Demonstration</h1>
    <h2>Wellcome: {user}</h2>
    <div id="content">
      
    </div>
    {/* {start?
    <div>
    <img id="bg1" style={{width: "25%"}} src="http://127.0.0.1:8001" alt=""/>
    <img id="bg2" style={{width: "25%"}} src="http://127.0.0.1:8002" alt=""/>
    <img id="bg3" style={{width: "25%"}} src="http://127.0.0.1:8003" alt=""/>
    <img id="bg4" style={{width: "25%"}} src="http://127.0.0.1:8004" alt=""/>
    </div>:null} */}
<div disabled={disable_click?disable_click:""}>
<button className="Start" id ='3' onClick={shoot} >Start Cam 3 feed</button>
<button className="Start" id ='4' onClick={shoot} >Start Cam 4 feed</button>
<button className="Start" id ='5' onClick={shoot} >Start Cam 5 feed</button>
<button className="Start" id ='6' onClick={shoot} >Start Cam 6 feed</button>
<button class="Stop" onClick={shoot} >Stop feed</button>

</div>
    </>
  )
}

export default Home