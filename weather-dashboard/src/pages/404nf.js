import React from 'react'
import { Link } from 'react-router-dom';
import '../styles/404nf.css'

function NotFound(){
    return(
        <>
        <div className="bg1"></div>
        <div className="centered">
            <h1 className="e404">404</h1>
            <h1 className="oops">OOPS! The page you were looking for is not here</h1>
            <br/>
            <h3 className="click17">Click the button to go back to Home</h3>
            <Link to="/home">
                <div className="button-home">
                    <button className='buttonhm' type='button'>Home</button>
                </div>
            </Link>
        </div>
    </>
    );
}

export default NotFound;