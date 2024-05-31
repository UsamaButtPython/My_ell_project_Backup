import React,{useRef,useEffect} from 'react'
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

function VideoPlayer({src}) {
  const transformComponentRef = useRef(null);
  var zoomValue=1
  const zoomRef = useRef(null);
  const videolink=src
  const videoRef = useRef(null);
  const timeElapsed = useRef(null);
  const duration=useRef(null);
  const progressBar = useRef(null);
  const seek = useRef(null);
  const seekTooltip = useRef(null);
  let videoElement=null;
  const updateScale = (e) => {
    const targetScale = parseFloat(e.target.value);
    const factor = Math.log(targetScale / zoomValue);
    const { zoomIn, zoomOut } = transformComponentRef.current;
    if (targetScale > zoomValue) {
      zoomIn(factor, 0);
    } else {
      zoomOut(-factor, 0);
    }

    zoomValue=targetScale
    zoomRef.current.value=targetScale
  };
  function playVid() { 
    if(videoElement.paused || videoElement.ended){
      videoElement.play(); 
      }
    else{
      videoElement.pause();
    }  
  } 
  function muteVid() { 
    if(videoElement.muted===false){
      videoElement.muted=true;
      }
    else{
      videoElement.muted=false;
    }  
  }
  function SetVolume(val)
    {
      videoElement.muted=false
      videoElement.volume = (val-50) / 100;
    }

  function formatTime(timeInSeconds) {
    const result = new Date(timeInSeconds * 1000).toISOString().substr(11, 8);
  
    return {
      minutes: result.substr(3, 2),
      seconds: result.substr(6, 2),
    };
  };
  function initializeVideo() {
    const videoDuration = Math.round(videoElement.duration);

    seek.current.setAttribute('max', videoDuration);
    progressBar.current.setAttribute('max', videoDuration);

    const time = formatTime(videoDuration);
    duration.current.innerText = `${time.minutes}:${time.seconds}`;
    duration.current.setAttribute('datetime', `${time.minutes}m ${time.seconds}s`)
  }  
  function updateTimeElapsed() {
    const time = formatTime(Math.round(videoElement.currentTime));
    timeElapsed.current.innerText = `${time.minutes}:${time.seconds}`;
    timeElapsed.current.setAttribute('datetime', `${time.minutes}m ${time.seconds}s`)
  }

  function updateProgress() {
    seek.current.value = Math.floor(videoElement.currentTime);
    progressBar.current.value = Math.floor(videoElement.currentTime);
  }
  function updateSeekTooltip(event) {
    const skipTo = Math.round((event.offsetX / event.target.clientWidth) * parseInt(event.target.getAttribute('max'), 10));
    seek.current.setAttribute('data-seek', skipTo)
    const t = formatTime(skipTo);
    seekTooltip.current.textContent = `${t.minutes}:${t.seconds}`;
    const rect = videoElement.getBoundingClientRect();
    seekTooltip.current.style.left = `${event.pageX - rect.left}px`;
  }
  function skipAhead(event) {
    // const seek = document.getElementById('seek');
    const skipTo = event.target.dataset.seek.current ? event.target.dataset.seek.current : event.target.value;
    videoElement.currentTime = skipTo;
    progressBar.current.value = skipTo;
    seek.current.value = skipTo;
  }

  useEffect(()=>{
      zoomRef.current.value=1
      videoElement=videoRef.current
      videoElement.addEventListener('timeupdate', (event) => {
      updateTimeElapsed()
      updateProgress()
    });


    seek.current.addEventListener('mousemove', (event) => {
      updateSeekTooltip(event)
    });
    seek.current.addEventListener('input', (event) => {
      skipAhead(event)
    });
  
  },[])

  return (
    <div className='fullscreen'>
    <TransformWrapper
    ref={transformComponentRef}
    onZoomStop={(e) => {
      zoomValue=e.state.scale
      zoomRef.current.value=e.state.scale
    }}
    onZoom={(e) => {
      zoomValue=e.state.scale
      zoomRef.current.value=e.state.scale

    }}
    >
        
        <TransformComponent>
        <video id="video" ref={videoRef} src={videolink} onLoadedMetadata={initializeVideo} muted autoPlay></video>
        </TransformComponent>
    </TransformWrapper>
    <div className="video-progress">
    <p>It's progress bar</p>
      <progress ref={progressBar} id="progress-bar" value="0" min="0"></progress>
    <p>It's seek bar</p>

      <input ref={seek} className="seek" id="seek" value="0" min="0" type="range" step="1"/>
      <div ref={seekTooltip} className="seek-tooltip" id="seek-tooltip">00:00</div>
    </div>
        <div className="time">
          <time ref={timeElapsed} id="time-elapsed">00:00</time>
          <span> / </span>
          <time ref={duration} id="duration">00:00</time>
        </div>
        <div className="tools">
          <p>It's zoom bar</p>
          <input type="range" min="1" max="8" step="0.01" ref={zoomRef} onChange={updateScale} />
              
            </div> 
        <div className='controls'>
          <button type='button' onClick={playVid} > play/pause</button>
          <button type='button' onClick={muteVid} > mute/unmute</button>
          <p>It's volume bar</p>

          <input  type="range" min="50" max="150" step="1"  onInput={(e)=>SetVolume(e.target.value)} onChange={(e)=>SetVolume(e.target.value)}></input>
        </div>
    </div>
  )
}


export default VideoPlayer