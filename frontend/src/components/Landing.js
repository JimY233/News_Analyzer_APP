import React, { Component } from 'react';
import { connect } from "react-redux";
import { Link } from "react-router-dom";

class Landing extends Component {
    renderContent() {
        switch (this.props.auth) {
            case null:
            case false:
            case undefined:
                return (
                    <div>
                        <h1>NewsAnalyzer</h1>
                        <div>
                            ToolKit for reporters!
                        </div>
                    </div>
                );
            default:
                return (
                    <div>
                        <h1>Welcome back, {this.props.auth}</h1>
                        Go to <Link to='/dashboard'>Dashboard</Link>
                    </div>
                )
        }
    }
    render() {
        return (
            <div style={{ textAlign: 'center' }}>
                {this.renderContent()}
            </div>
        );
    }
    
}

function mapStateToProps({auth}) {
    return { auth };
}
export default connect(mapStateToProps)(Landing);