import React, { Component } from "react";
import { connect } from 'react-redux';
import { Link } from "react-router-dom";

class Header extends Component {
    renderContent() { // helper to decide what to show depend on logged in or not
        switch (this.props.auth) {
            case null:
                return 'deciding';
            case false:
                return (
                    <li><Link to='/login'>Login</Link></li>
                );
            default:
                console.log('current props for Header is ', this.props)
                return [
                    <li key="3" style={{ margin: '0px 10px' }}>
                        Currently Logged In as {this.props.auth}
                    </li>,
                    <li key='2'><a href='http://localhost:5000/api/logout'>Logout</a></li>
                ];
        }
    }
    render() {
        return (
            <nav style={{marginBottom:'60px'}}>
                <div className="nav-wrapper">
                    <Link 
                        to={this.props.auth ? "/dashboard" : "/"} 
                        className="left brand-logo"
                    >
                        NewsAnalyzer
                    </Link>
                    <ul className="right">
                        {this.renderContent()}
                    </ul>
                </div>
            </nav>
        );
    }
}
function mapStateToProps({auth}) {
    return { auth };
}
export default connect(mapStateToProps)(Header);