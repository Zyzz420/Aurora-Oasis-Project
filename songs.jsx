import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Songs() {
  const [songs, setSongs] = useState([]);
    const url = './dashboard'
  useEffect(() => {
    axios.get('/api/Songs/songs') // Replace with your Flask route
      .then((response) => {
        setSongs(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Songs</h1>
      <ul>
        {songs.map((song) => (
          <li key={song.id}>{song.title} - {song.artist}</li>
        ))}
      </ul>
    </div>
  );
}

export default Songs;
