import React from "react";
import TimeInput from "react-input-time";

const TimeComp = ({purpose}) => {
    const onFocus= (e) =>{
        e.target.type="time"
    }

    const onBlur=(e)=>{
    const event=e.target
    if(!event.value){
        event.type="text"
        }
    }      
    return (
        <TimeInput
        onFocus={onFocus} 
        onBlur={onBlur} 
        className="input-time"
        initialTime=""

        placeholder={purpose}
        input={<input  style={{width:"100px"}}type="text" />}
        />
    )
}

export default TimeComp