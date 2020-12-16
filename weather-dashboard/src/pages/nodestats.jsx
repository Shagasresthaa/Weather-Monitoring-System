import React from 'react'
import '../styles/nodestats.css'
import NavBar from '../components/NavBar/NavBar'

function NodeStats(){
    return(
        <>
        <NavBar/>
        <div className="bg5"></div>
        <div className="centered6">
            <h1>Node Statistics Page</h1>
        </div>
        </>
    );
}

export default NodeStats;