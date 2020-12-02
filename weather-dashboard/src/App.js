import './App.css';
import React from 'react';

import NavBar from './components/NavBar/NavBar'
import {BrowserRouter as Router,Switch,Route, Redirect} from 'react-router-dom'

import Home from './pages/home'
import About from './pages/about'
import DataInfo from './pages/datainfo'
import NodeDash from './pages/nodedash'
import NodeStats from './pages/nodestats'
import NotFound from './pages/404nf'

function App() {
  return (
    <Router>
      <NavBar/>
    <div className="App">
      <Switch>
        <Route exact path="/">
          <Redirect to="/home" />
        </Route>
        <Route path='/home' exact component={Home}/>
        <Route path='/about' exact component={About}/>
        <Route path='/datainf' exact component={DataInfo}/>
        <Route path='/nodedash' exact component={NodeDash}/>
        <Route path='/nodestats' exact component={NodeStats}/>
        <Route path='/404' exact component={NotFound}/>
        <Redirect to="/404"/>
      </Switch>
    </div>
    </Router>
  );
}

export default App;
