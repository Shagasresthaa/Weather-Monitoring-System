import React from 'react'
import '../styles/home.css'

import Card from '../components/cards/CardsUI'

import Database from '../assets/database.png'
import Node from '../assets/img-servers.png'
import TotNodes from '../assets/tnodes.png'
import Dummy from '../assets/dummy.jpeg'

function Home() {
  return (
    <>
      <div className="bg3"></div>
      <div className="centered4">
        <div className="row">
          <div className="col-md-4">
            <Card img={Database} h4="Database Status" p="Active"/>
          </div>
          <div className="col-md-4">
            <Card img={Node} h4="Active Nodes" p="Active"/>
          </div>
          <div className="col-md-4">
            <Card img={TotNodes} h4="Total Nodes" p="Active"/>
          </div>
        </div>
      </div>
    </>
  );
}

export default Home;