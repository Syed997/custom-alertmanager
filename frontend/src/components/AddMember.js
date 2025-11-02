import React, { useState } from "react";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000/api";

const AddMember = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    group_id: "",
    name: "",
    mail: "",
    m_number: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (
      !formData.group_id ||
      !formData.name ||
      !formData.mail ||
      !formData.m_number
    )
      return;

    try {
      const res = await fetch(`${API_BASE}/members/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (res.ok) {
        alert("Member added successfully!");
        setFormData({ group_id: "", name: "", mail: "", m_number: "" });
        onSuccess();
      } else {
        const error = await res.json();
        alert("Error: " + (error.error || "Failed to add member"));
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
      <input
        type="number"
        name="group_id"
        placeholder="Group ID"
        value={formData.group_id}
        onChange={handleChange}
        required
      />
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
        name="m_number"
        placeholder="Mobile Number"
        value={formData.m_number}
        onChange={handleChange}
        required
      />
      <button type="submit">Add Member</button>
    </form>
  );
};

export default AddMember;
