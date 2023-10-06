import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function Profiles() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const url = '/profiles';

    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setUsers(data.users);
      })
      .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
      });
  }, []);

  return (
    <div>
      <h1>User Profiles</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}

function Profile() 
{
    const { user_id } = useParams();
    const [user, setUser] = useState({});
    const [songs, setSongs] = useState([]);
    const [playlist, setPlaylist] = useState({});

    const url = '/profile/<int:user_id>';

    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setUsers(data.users);
      })
      .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
      });
  }, [user_id]);

  return (
    <div>
      {/* Show profile, songs, and playlist information */}
    </div>
  );
}
export default Profile;
