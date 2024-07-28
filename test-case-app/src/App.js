import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [testCases, setTestCases] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTestCases();
  }, []);

  const fetchTestCases = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/testcases');
      setTestCases(response.data);
    } catch (err) {
      setError('Failed to fetch test cases');
      console.error(err);
    }
  };

  const handleStatusChange = async (id, status) => {
    try {
      await axios.put(`http://localhost:5000/api/testcases/${id}`, { status });
      fetchTestCases(); // Refresh the list after update
    } catch (err) {
      setError('Failed to update test case');
      console.error(err);
    }
  };

  return (
    <div className="App">
      <h1>Test Cases</h1>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Test Case Name</th>
            <th>Estimate Time</th>
            <th>Module</th>
            <th>Priority</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {testCases.map((testCase) => (
            <tr key={testCase.id}>
              <td>{testCase.name}</td>
              <td>{testCase.estimate_time}</td>
              <td>{testCase.module}</td>
              <td>{testCase.priority}</td>
              <td>
                <select
                  value={testCase.status}
                  onChange={(e) => handleStatusChange(testCase.id, e.target.value)}
                >
                  <option value="Select">Select</option>
                  <option value="PASS">PASS</option>
                  <option value="FAIL">FAIL</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
