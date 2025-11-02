import React, { useState } from "react";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000/api";

const EditMember = ({ memberId, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    name: "",
    mail: "",
    m_number: "",
    group_id: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const updateData = {};
    if (formData.name) updateData.name = formData.name;
    if (formData.mail) updateData.mail = formData.mail;
    if (formData.m_number) updateData.m_number = formData.m_number;
    if (formData.group_id) updateData.group_id = parseInt(formData.group_id);

    if (Object.keys(updateData).length === 0) return;

    try {
      const res = await fetch(`${API_BASE}/members/${memberId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updateData),
      });
      if (res.ok) {
        alert("Member updated successfully!");
        onSuccess();
      } else {
        const error = await res.json();
        alert("Error: " + (error.error || "Failed to update member"));
      }
    } catch (error) {
      alert("Error: " + error.message);
    }
    onCancel();
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="modal">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="New Name (leave blank to skip)"
          onChange={handleChange}
        />
        <input
          type="email"
          name="mail"
          placeholder="New Email (leave blank to skip)"
          onChange={handleChange}
        />
        <input
          type="text"
          name="m_number"
          placeholder="New Mobile (leave blank to skip)"
          onChange={handleChange}
        />
        <input
          type="number"
          name="group_id"
          placeholder="New Group ID (leave blank to skip)"
          onChange={handleChange}
        />
        <button type="submit">Update</button>
        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      </form>
    </div>
  );
};

export default EditMember;
