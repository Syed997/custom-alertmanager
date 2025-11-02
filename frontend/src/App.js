import React, { useEffect, useState } from "react";
import "./App.css";
import AddGroup from "./components/AddGroup";
import AddMember from "./components/AddMember";
import MemberList from "./components/MemberList";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000/api";

function App() {
  const [groups, setGroups] = useState([]);
  const [members, setMembers] = useState([]);

  const loadData = async () => {
    try {
      // Fetch members (groups not needed since members include "group" name)
      const membersRes = await fetch(`${API_BASE}/members/`);
      if (!membersRes.ok) throw new Error("Failed to fetch members");
      const membersData = await membersRes.json();
      console.log("Fetched members:", membersData); // Debug: Verify data here

      // Group members by "group" name (string)
      const groupsMap = {};
      membersData.forEach((m) => {
        const gName = m.group;
        if (gName && !groupsMap[gName]) {
          groupsMap[gName] = {
            group: gName,
            id: null, // Not used for display; add if you fetch groups later
            members: [],
          };
        }
        if (gName) {
          groupsMap[gName].members.push(m);
        }
      });

      const groupedGroups = Object.values(groupsMap);
      console.log("Grouped groups:", groupedGroups); // Debug: Verify grouping

      setGroups(groupedGroups);
      setMembers(membersData);
    } catch (error) {
      console.error("Error loading data:", error);
      alert("Error loading data: " + error.message);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const refreshData = () => loadData();

  return (
    <div className="App">
      <h1>Groups and Members</h1>
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
