import { useState } from 'react'
import './App.css'

function App() {  
  const [selectedFile, setSelectedFile] = useState(null)  
  const [videoURL, setVideoURL] = useState('')
  const [responseMessage, setResponseMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [processedVideoURL, setProcessedVideoURL] = useState('')

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    setSelectedFile(file)
    setVideoURL(URL.createObjectURL(file))
  }

  const handleEndpointCall = async () => {
    if (!selectedFile) {
      setResponseMessage('Please select a file first')
      return
    }
  
    const formData = new FormData()
    formData.append('video', selectedFile)
  
    setLoading(true)
    try {
      const response = await fetch('http://127.0.0.1:5000/upload_video', {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      setResponseMessage(data.message)
      
      // Extract only the filename from the absolute file path
      const outputFilename = data.output_filename.includes('\\')
        ? data.output_filename.split('\\').pop()
        : data.output_filename.split('/').pop();
      
      console.log("Extracted filename:", outputFilename);
      
      // Build the URL with the correct endpoint that serves the processed video
      setProcessedVideoURL(`http://127.0.0.1:5000/processed_videos/${outputFilename}`)
    } catch (error) {
      setResponseMessage('Error calling endpoint')
    } finally {
      setLoading(false)
    }
  };
  
  return (
    <>
      <h1>Cristiano Ronaldo football match marking</h1>
      <h2>This website uses pre-trained YOLO model to mark Cristiano Ronaldo in a video</h2>
      
      <div className="upload-section">
        <h2>Please upload a video file (.mp4)</h2>
        <input type="file" accept="video/*" onChange={handleFileChange} />                
      </div>      

      {videoURL && (
        <div className="video-section">          
          <video width="600" controls>
            <source src={videoURL} type="video/mp4" />
            Your browser does not support the video tag.
          </video>          
        </div>
      )}

      <div>
        <button onClick={handleEndpointCall}>Mark player</button>
        {responseMessage && <p>{responseMessage}</p>}
      </div>

      {loading && <div className="loading">Loading...</div>}

      {processedVideoURL && (
        <div className="processed-video-section">
          <h2>Processed Video</h2>
          <video width="600" controls>
            <source src={processedVideoURL} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
      
    </>
  )
}

export default App
