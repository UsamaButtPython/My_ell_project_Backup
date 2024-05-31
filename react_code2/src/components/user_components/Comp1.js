import React from 'react'

function Comp1({test,handleSetTest}) {
  return (
    <>
    <div>Comp1={test}</div>
    <input onChange={handleSetTest} value={test} />
    {/* <button onClick={setTest("mola")}></button> */}
    
    </>
  )
}

export default Comp1