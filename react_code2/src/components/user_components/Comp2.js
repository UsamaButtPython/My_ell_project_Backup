import React from 'react'

function Comp2({test,handleSetTest}) {
    
  return (
    <>
    <div>Comp2={test}</div>
    <input onChange={handleSetTest} value={test} />
    </>

  )
}

export default Comp2