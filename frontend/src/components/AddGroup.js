import React, { useState } from "react";
import { toast } from "react-toastify";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000";

const AddGroup = ({ onSuccess }) => {
  const [groupName, setGroupName] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!groupName) return;

    // const token = localStorage.getItem("access_token");
    // console.log("Using token:", token);
    try {
      const token = localStorage.getItem("access_token");
      console.log("Using token:", token);
      const res = await fetch(`${API_BASE}/groups/add`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ group: groupName }),
      });
      if (res.ok) {
        toast.success("Group added successfully!");
        setGroupName("");
        onSuccess();
      } else {
        const error = await res.json();
        // alert("Error: " + (error.error || "Failed to add group"));
        toast.error("Error: " + (error.error || "Failed to add group"));
      }
    } catch (error) {
      // alert("Error: " + error.message);
      toast.error("Error: " + error.message);
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
