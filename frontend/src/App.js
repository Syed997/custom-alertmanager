import React, { useEffect, useState } from "react";
import "./App.css";
import Login from "./components/Login";
import Signup from "./components/Signup";
import AddGroup from "./components/AddGroup";
import AddMember from "./components/AddMember";
import MemberList from "./components/MemberList";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [groups, setGroups] = useState([]);
  const [members, setMembers] = useState([]);

  // Check if user is already logged in
  useEffect(() => {
    // localStorage.setItem("access_token", "demoToken");
    // TODO: need to check by changing the token
    // TODO: auto logout after token expiry
    // TODO: make the group visible(currently empty group not visible)
    const token = localStorage.getItem("access_token");
    
    if(token && token !== undefined){
      setIsAuthenticated(true);
    }else{
      setIsAuthenticated(false);
    }
  }, []);

  const loadData = async () => {
    const token = localStorage.getItem("access_token");
    if (!token || token === undefined) {
      console.error("No token found");
      return;
    }

    try {
      const membersRes = await fetch(`${API_BASE}/members/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!membersRes.ok) {
        if (membersRes.status === 401) {
          handleLogout();
          return;
        }
        throw new Error("Failed to fetch members");
      }

      const membersData = await membersRes.json();
      console.log("Fetched members:", membersData);

      const groupsMap = {};
      membersData.forEach((m) => {
        const gName = m.group;
        if (gName && !groupsMap[gName]) {
          groupsMap[gName] = {
            group: gName,
            id: null,
            members: [],
          };
        }
        if (gName) {
          groupsMap[gName].members.push(m);
        }
      });

      const groupedGroups = Object.values(groupsMap);
      console.log("Grouped groups:", groupedGroups);
      setGroups(groupedGroups);
      setMembers(membersData);
    } catch (error) {
      console.error("Error loading data:", error);
      alert("Error loading data: " + error.message);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadData();
    }
  }, [isAuthenticated]);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleSignupSuccess = () => {
    setShowSignup(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
    setGroups([]);
    setMembers([]);
  };

  const refreshData = () => loadData();

  if (!isAuthenticated) {
    return (
      <div className="App">
        {showSignup ? (
          <Signup
            onSignupSuccess={handleSignupSuccess}
            onSwitchToLogin={() => setShowSignup(false)}
          />
        ) : (
          <Login
            onLoginSuccess={handleLoginSuccess}
            onSwitchToSignup={() => setShowSignup(true)}
          />
        )}
      </div>
    );
  }

  return (
    <div className="App">
      <div className="header">
        <h1>Groups and Members</h1>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </div>
      <div className="buttons">
        <AddGroup onSuccess={refreshData} />
        <AddMember onSuccess={refreshData} />
      </div>
      {groups.length === 0 ? (
        <p>No groups or members found. Add some to get started!</p>
      ) : (
        <MemberList groups={groups} onUpdate={refreshData} />
      )}
    </div>
  );
}

export default App;
