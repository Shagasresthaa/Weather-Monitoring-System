import React, { Component } from 'react'
import { MenuItems } from './MenuItems'
import './NavBar.css'
import {Link} from 'react-router-dom'

class NavBar extends Component{
    state = {clicked: false}

    handleClick = () => {
        this.setState({clicked: !this.state.clicked})
    }

    render(){
        return(
            <nav className="NavbarItems">
                <h1 className="navbar-logo">
                    <Link to='/home' className='nvlink' style={{pointerEvents:"none"}}>
                    Dashboard
                    <i className="fas fa-cloud">
                    </i>
                    </Link>
                </h1>
                <div className="menu-icon" onClick={this.handleClick}>
                    <i className={this.state.clicked ? 'fas fa-times' : 'fas fa-bars'}></i>
                </div>
                <ul className={this.state.clicked ? 'nav-menu active' : 'nav-menu'} >
                    {MenuItems.map((item, index) => {
                        return (<Link to={item.to} className="nvlink">
                        <li key={index} className={item.cName} href={item.url} onClick={this.handleClick}>
                                {item.title}
                        </li>
                        </Link>
                        
                        )
                    })}
                </ul>
            </nav>
            
        )
    }
}

export default NavBar