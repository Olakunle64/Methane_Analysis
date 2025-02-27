// src/FileUpload.js
import React, { useState } from 'react';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '../FileUpload.css'; // Import the CSS file for styling

// toast.configure();

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState('');


  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a file!');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('email', email);

    setLoading(true);
    try {
      console.log(email);
      const response = await axios.post(
        'http://127.0.0.1:5000/upload', // Replace with actual API endpoint
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer YOUR_API_KEY', // Replace with actual API key
          },
        }
      );
      // console.log(email);
      console.log(response.data);
      toast.success('File uploaded successfully!');
      alert("File uploaded successfully!");
    } catch (error) {
      toast.error('Upload failed!');
      alert("Upload failed!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <img src="./logo.png" alt="Bovi-Analytics Logo" className="logo" />
      <h1>Bovi-Analytics Lab File Upload</h1>
      <input type="file" onChange={handleFileChange} />
      <input type='email' placeholder='Enter your email' required onChange={(e) => setEmail(e.target.value)}/>
      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload'}
      </button>
    </div>
  );
};

export default FileUpload;
