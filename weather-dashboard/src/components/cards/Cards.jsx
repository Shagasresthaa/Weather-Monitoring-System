import React, { Component } from 'react'
import Card from './CardsUI'

import img1 from '../../assets/database.png'
import img2 from '../../assets/tnodes.png'
import img3 from '../../assets/img-servers.png'
import img4 from '../../assets/dummy.jpeg'

class Cards extends Component {
    render() {
        return (
            <div className="container-fluid d-flex justify-content-center">
                <div className="row">
                    <div className="col-md-4">
                        <Card img={img1} h4="Card 1" p="This is p for Card 1" />
                    </div>
                    <div className="col-md-4">
                        <Card img={img2} h4="Card 2" p="This is p for Card 2" />
                    </div>
                    <div className="col-md-4">
                        <Card img={img3} h4="Card 3" p="This is p for Card 3" />
                    </div>
                    <div className="col-md-4">
                        <Card img={img4} h4="Card 4" p="This is p for Card 4" />
                    </div>
                </div>
            </div>
        );
    }
}

export default Cards;