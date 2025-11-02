import React, { useState } from "react";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000/api";

const AddGroup = ({ onSuccess }) => {
  const [groupName, setGroupName] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!groupName) return;

    try {
      const res = await fetch(`${API_BASE}/groups/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ group: groupName }),
      });
      if (res.ok) {
        alert("Group added successfully!");
        setGroupName("");
        onSuccess();
      } else {
        const error = await res.json();
        alert("Error: " + (error.error || "Failed to add group"));
      }
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Group Name"
        value={groupName}
        onChange={(e) => setGroupName(e.target.value)}
        required
      />
      <button type="submit">Add Group</button>
    </form>
  );
};

export default AddGroup;
