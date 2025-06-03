import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [showSuspiciousOnly, setShowSuspiciousOnly] = useState(false);

  // Fetch transactions from backend API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:8080/transactions");
        const data = await res.json();
        setTransactions(data);
      } catch (error) {
        console.error("Failed to fetch transactions:", error);
      }
    };

    fetchData();

    // Poll every 10 seconds for real-time updates
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const toggleFilter = () => {
    setShowSuspiciousOnly((prev) => !prev);
  };

  // Filter suspicious transactions if toggle is on
  const filteredTransactions = showSuspiciousOnly
    ? transactions.filter((tx) => tx.amount > 50000)
    : transactions;

  return (
    <div className="container">
      <h1>Transaction Dashboard</h1>

      <button className="filter-button" onClick={toggleFilter}>
        {showSuspiciousOnly ? "Show All Transactions" : "Show Suspicious Only"}
      </button>

      <ul className="transaction-list">
        {filteredTransactions.length === 0 && (
          <li>No transactions to display</li>
        )}
        {filteredTransactions.map((tx) => (
          <li
            key={tx.id || `${tx.customer_name}-${tx.timestamp}`}
            className={`transaction-item ${
              tx.amount > 50000 ? "suspicious" : ""
            }`}
          >
            <div>
              <strong>{tx.customer_name}</strong> <br />
              <small>{tx.location}</small>
            </div>
            <div>
              <span>{tx.amount.toLocaleString()} SAR</span> <br />
              <small>{new Date(tx.timestamp).toLocaleString()}</small>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
