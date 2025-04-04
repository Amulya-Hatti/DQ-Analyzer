import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  FiHome, 
  FiDatabase, 
  FiList, 
  FiCheckSquare,
  FiBarChart2
} from 'react-icons/fi';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-menu">
        <NavLink to="/dashboard" className={({isActive}) => isActive ? 'sidebar-link active' : 'sidebar-link'}>
          <FiHome className="sidebar-icon" />
          <span className="sidebar-text">Dashboard</span>
        </NavLink>
        
        <NavLink to="/tables" className={({isActive}) => isActive ? 'sidebar-link active' : 'sidebar-link'}>
          <FiDatabase className="sidebar-icon" />
          <span className="sidebar-text">Tables</span>
        </NavLink>
        
        <NavLink to="/rules" className={({isActive}) => isActive ? 'sidebar-link active' : 'sidebar-link'}>
          <FiList className="sidebar-icon" />
          <span className="sidebar-text">Validation Rules</span>
        </NavLink>
        
        <NavLink to="/validations" className={({isActive}) => isActive ? 'sidebar-link active' : 'sidebar-link'}>
          <FiCheckSquare className="sidebar-icon" />
          <span className="sidebar-text">Run Validations</span>
        </NavLink>
        
        <NavLink to="/reports" className={({isActive}) => isActive ? 'sidebar-link active' : 'sidebar-link'}>
          <FiBarChart2 className="sidebar-icon" />
          <span className="sidebar-text">Reports</span>
        </NavLink>
      </div>
      
      <div className="sidebar-footer">
        <span className="version-text">v1.0.0</span>
      </div>
    </div>
  );
};

export default Sidebar;