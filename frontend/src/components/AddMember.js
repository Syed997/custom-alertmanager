import React, { useState, useEffect } from "react";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000";

const AddMember = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    group: "",
    name: "",
    mail: "",
    mobile: "",
  });

  const [groups, setGroups] = useState([]);
  const [loadingGroups, setLoadingGroups] = useState(true);

  // 🔹 Fetch groups when component mounts
  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const res = await fetch(`${API_BASE}/groups/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!res.ok) throw new Error("Failed to load groups");
        const data = await res.json();
        setGroups(data);
      } catch (err) {
        alert("Error fetching groups: " + err.message);
      } finally {
        setLoadingGroups(false);
      }
    };
    fetchGroups();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.group || !formData.name || !formData.mail || !formData.mobile)
      return;

    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(`${API_BASE}/members/add`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (res.ok) {
        alert("✅ Member added successfully!");
        setFormData({ group: "", name: "", mail: "", mobile: "" });
        onSuccess();
      } else {
        const error = await res.json();
        alert("❌ Error: " + (error.error || "Failed to add member"));
      }
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Group Dropdown */}
      <select
        name="group"
        value={formData.group}
        onChange={handleChange}
        required
        disabled={loadingGroups}
      >
        <option value="">
          {loadingGroups ? "Loading groups..." : "Select a group"}
        </option>
        {groups.map((g) => (
          <option key={g.id} value={g.group}>
            {g.group}
          </option>
        ))}
      </select>

      <input
        type="text"
        name="name"
        placeholder="Name"
        value={formData.name}
        onChange={handleChange}
        required
      />

      <input
        type="email"
        name="mail"
        placeholder="Email"
        value={formData.mail}
        onChange={handleChange}
        required
      />

      <input
        type="text"
        name="mobile"
        placeholder="Mobile Number"
        value={formData.mobile}
        onChange={handleChange}
        required
      />

      <button type="submit">Add Member</button>
    </form>
  );
};

export default AddMember;
