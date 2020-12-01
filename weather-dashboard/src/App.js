import './App.css';
import React from 'react';

import NavBar from './components/NavBar/NavBar'
import {BrowserRouter as Router,Switch,Route} from 'react-router-dom'

import Home from './pages/home'
import About from './pages/about'
import DataInfo from './pages/datainfo'
import NodeDash from './pages/nodedash'
import NodeStats from './pages/nodestats'

function App() {
  
  return (
    <Router>
    <div className="App">
    <NavBar/>
      <Switch>
        <Route path='/' exact component={Home}/>
        <Route path='/about' exact component={About}/>
        <Route path='/datainf' exact component={DataInfo}/>
        <Route path='/nodedash' exact component={NodeDash}/>
        <Route path='/nodestats' exact component={NodeStats}/>
      </Switch>
    </div>
    </Router>
  );
}

export default App;
