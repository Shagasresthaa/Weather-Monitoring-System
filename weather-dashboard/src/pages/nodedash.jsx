import React from 'react'
import '../styles/nodedash.css'
import NavBar from '../components/NavBar/NavBar'

function NodeDash(){
    return(
        <>
        <NavBar/>
        <div className="bg4"></div>
        <div className="centered5">
            <h1>Node Dashboard Page</h1>
        </div>
        </>
    );
}

export default NodeDash;