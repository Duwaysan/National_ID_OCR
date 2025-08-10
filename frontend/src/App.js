import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const API = "http://127.0.0.1:8000";

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setError("");
  };

  const loadRecords = async () => {
    try {
      const { data } = await axios.get(`${API}/records`);
      setRecords(data || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadRecords();
  }, []);

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${API}/upload-id/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
      await loadRecords(); // refresh table after successful upload
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      {/* HEADER */}
      <header style={styles.header}>
        <h1 style={styles.headerTitle}>ID OCR Extraction</h1>
      </header>

      {/* MAIN CONTENT */}
      <main style={styles.main}>
        {/* Upload */}
        <div style={styles.uploadSection}>
          <input type="file" onChange={handleFileChange} accept="image/*" style={styles.fileInput} />
          <button onClick={handleUpload} disabled={loading} style={styles.uploadButton}>
            {loading ? "Processing..." : "Upload"}
          </button>
          {error && <p style={styles.error}>{error}</p>}
        </div>

        {/* Result (face + info) */}
        {result && (
          <div style={styles.resultContainer}>
            {/* Face Image */}
            <div style={styles.faceCard}>
              {result.face_image && result.face_image !== "Not detected" ? (
                <img
                  src={`data:image/jpeg;base64,${result.face_image}`}
                  alt="Detected Face"
                  style={styles.faceImage}
                />
              ) : (
                <p>No face found</p>
              )}
            </div>

            {/* Info Table */}
            <div style={styles.tableCard}>
              <table style={styles.table}>
                <tbody>
                  <tr>
                    <th style={styles.tableHeader}>Full Name</th>
                    <td style={styles.tableCell}>{result.full_name}</td>
                  </tr>
                  <tr>
                    <th style={styles.tableHeader}>ID Number</th>
                    <td style={styles.tableCell}>{result.id_number}</td>
                  </tr>
                  <tr>
                    <th style={styles.tableHeader}>Date of Birth</th>
                    <td style={styles.tableCell}>{result.dob}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Stored IDs */}
        <section style={{ marginTop: 30 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
            <h3 style={{ margin: 0 }}>Stored IDs</h3>
            <button onClick={loadRecords} style={styles.refreshBtn}>Refresh</button>
          </div>

          <div style={{ overflowX: "auto" }}>
            <table style={{ ...styles.table, width: "100%", minWidth: 700 }}>
              <thead>
                <tr>
                  <th style={styles.tableHeader}>ID Number</th>
                  <th style={styles.tableHeader}>Full Name</th>
                  <th style={styles.tableHeader}>Date of Birth</th>
                  <th style={styles.tableHeader}>Face</th>
                </tr>
              </thead>
              <tbody>
                {records.length === 0 ? (
                  <tr>
                    <td colSpan="4" style={styles.tableCell}>No records yet.</td>
                  </tr>
                ) : (
                  records.map((r) => (
                    <tr key={r.id_number}>
                      <td style={styles.tableCell}>{r.id_number}</td>
                      <td style={styles.tableCell}>{r.full_name}</td>
                      <td style={styles.tableCell}>{r.dob}</td>
                      <td style={styles.tableCell}>
                        {r.has_face ? (
                          <img
                            src={`${API}/records/${r.id_number}/face`}
                            alt="face"
                            style={{ width: 50, height: 50, objectFit: "cover", borderRadius: 6 }}
                          />
                        ) : (
                          "—"
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer style={styles.footer}>
        <p>© {new Date().getFullYear()} ID OCR Extraction | Built using React & FastAPI</p>
      </footer>
    </div>
  );
}

const styles = {
  page: {
    fontFamily: "Arial, sans-serif",
    backgroundColor: "#f8fafc",
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
  },
  header: {
    backgroundColor: "#0f172a",
    padding: "20px 0",
    textAlign: "center",
    color: "white",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.2)",
  },
  headerTitle: {
    margin: 0,
    fontSize: "24px",
  },
  main: {
    flex: 1,
    padding: "20px",
    maxWidth: "1000px",
    margin: "0 auto",
  },
  uploadSection: {
    textAlign: "center",
    marginBottom: "20px",
  },
  fileInput: {
    marginBottom: "10px",
  },
  uploadButton: {
    backgroundColor: "#f97316",
    color: "white",
    padding: "10px 25px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  refreshBtn: {
    backgroundColor: "#f97316",
    color: "#fff",
    border: "none",
    padding: "8px 14px",
    borderRadius: 6,
    cursor: "pointer",
    fontWeight: 600,
  },
  error: {
    color: "red",
    marginTop: "10px",
  },
  resultContainer: {
    display: "flex",
    gap: "20px",
    justifyContent: "center",
    alignItems: "flex-start",
    flexWrap: "wrap",
  },
  faceCard: {
    backgroundColor: "white",
    padding: "10px",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
  },
  faceImage: {
    width: "250px",
    height: "auto",
    borderRadius: "8px",
  },
  tableCard: {
    backgroundColor: "white",
    padding: "15px",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
  },
  table: {
    borderCollapse: "collapse",
  },
  tableHeader: {
    backgroundColor: "#0f172a",
    color: "white",
    padding: "12px 16px",
    border: "1px solid #e5e7eb",
    textAlign: "left",
  },
  tableCell: {
    padding: "10px 12px",
    border: "1px solid #e5e7eb",
    backgroundColor: "#f8fafc",
  },
  footer: {
    backgroundColor: "#0f172a",
    color: "white",
    textAlign: "center",
    padding: "10px 0",
    marginTop: "auto",
    fontSize: "14px",
  },
};

export default App;
