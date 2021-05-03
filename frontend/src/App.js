import React, {Component} from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import { connect } from 'react-redux';
import * as actions from './action';

import Header from "./components/Header";
import Landing from "./components/Landing";
import Dashboard from "./components/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register"

class App extends Component {
    componentDidMount() {
        this.props.fetchUser();
    }
    render() {
        return (
            <Router> 
                <div className="container">
                    <Header/>
                    <Route exact path="/" component={Landing} />
                    <Route exact path="/dashboard" component={Dashboard}/>
                    <Route exact path="/login"  component={Login}/>
                    <Route path="/signup" component={Register}/>
                </div>
            </Router>
        );
    }
}

export default connect(null, actions)(App);