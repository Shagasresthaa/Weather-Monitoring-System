import React from 'react'
import '../styles/about.css'
import NavBar from '../components/NavBar/NavBar'

function About(){
    return(
        <>
        <NavBar/>
        <div className="bg"></div>
        <div className="centered2">
            <h1>About Me Page</h1>
        </div>
        </>
    );
}

export default About;