import React, { useContext } from "react";
import Context from "../context/Context";
import { useHistory } from "react-router";
import { globalVars } from '../util/common';
const Navbar = () => {
    const { addSideBarClass, setAddSideBarClass } = useContext(Context);
    const history = useHistory();

    const logoutClickHandler = async (evt) => {
        evt.preventDefault();

        var response = await fetch(globalVars.urls.baseURL+'/logout')

        var data = await response.json()
        
        if(data.return === 'logged out'){
            localStorage.clear();
            history.push('/login')
        }
    }

    return (
        <>
            <nav className="sb-topnav navbar navbar-expand navbar-dark bg-dark">
                <a className="navbar-brand" href="index.html">Stamp Search Engine </a>
                <button onClick={() => { setAddSideBarClass(!addSideBarClass) }} className="btn btn-link btn-sm order-1 order-lg-0" id="sidebarToggle" href="#"><i className="fas fa-bars"></i></button>
                {/* <!-- Navbar Search--> */}
                <form className="d-none d-md-inline-block form-inline ml-auto mr-0 mr-md-3 my-2 my-md-0">
                    <div className="input-group">
                        <input className="form-control" type="text" placeholder="Search for..." aria-label="Search" aria-describedby="basic-addon2" />
                        <div className="input-group-append">
                            <button className="btn btn-primary" type="button"><i className="fas fa-search"></i></button>
                        </div>
                    </div>
                </form>
                {/* <!-- Navbar--> */}
                <ul className="navbar-nav ml-auto ml-md-0">
                    <li className="nav-item dropdown">
                        <a className="nav-link dropdown-toggle" id="userDropdown" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i className="fas fa-user fa-fw"></i></a>
                        <div className="dropdown-menu dropdown-menu-right" aria-labelledby="userDropdown">
                            <a className="dropdown-item" href="#">Settings</a>
                            <a className="dropdown-item" href="#">Activity Log</a>
                            <div className="dropdown-divider"></div>
                            <a className="dropdown-item" onClick={logoutClickHandler}>Logout</a>
                        </div>
                    </li>
                </ul>
            </nav>

        </>
    );
};

export default Navbar;
