import React, { useState } from "react";
import EditMember from "./EditMember";

const MemberList = ({ groups, onUpdate }) => {
  const [editingId, setEditingId] = useState(null);

  const handleDelete = async (memberId) => {
    if (!window.confirm("Are you sure you want to delete this member?")) return;

    const API_BASE =
      process.env.REACT_APP_API_BASE || "http://localhost:5000";

    try {
      const res = await fetch(`${API_BASE}/members/${memberId}`, {
        method: "DELETE",
      });
      if (res.ok) {
        alert("Member deleted successfully!");
        onUpdate();
      } else {
        const error = await res.json();
        alert("Error: " + (error.error || "Failed to delete member"));
      }
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  const startEdit = (id) => setEditingId(id);
  const cancelEdit = () => setEditingId(null);

  return (
    <div>
      {groups.map((group) => (
        <div key={group.group} className="group">
          {" "}
          {/* Key by group name */}
          <h2>{group.group}</h2> {/* Removed ID since it's null/not used */}
          <div className="members">
            {group.members.map((member) => (
              <div key={member.id} className="member">
                {editingId === member.id ? (
                  <EditMember
                    memberId={member.id}
                    onSuccess={onUpdate}
                    onCancel={cancelEdit}
                  />
                ) : (
                  <>
                    <span className="name">Name: { member.name}</span>
                    <span className="mail">Mail: {member.mail}</span>
                    <span className="mobile">Mobile: {member.mobile}</span>{" "}
                    {/* Fixed: Use "mobile" */}
                    <div className="icons">
                      <button
                        className="edit-btn"
                        onClick={() => startEdit(member.id)}
                      >
                        Edit
                      </button>
                      <button
                        className="delete-btn"
                        onClick={() => handleDelete(member.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default MemberList;
