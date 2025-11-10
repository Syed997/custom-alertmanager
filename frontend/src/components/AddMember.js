import React, { useState } from "react";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000";

const AddMember = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    group: "",
    name: "",
    mail: "",
    mobile: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (
      !formData.group ||
      !formData.name ||
      !formData.mail ||
      !formData.mobile
    )
      return;

    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(`${API_BASE}/members/add`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });
      if (res.ok) {
        alert("Member added successfully!");
        setFormData({ group: "", name: "", mail: "", mobile: "" });
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
        type="text"
        name="group"
        placeholder="Group Name"
        value={formData.group}
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
