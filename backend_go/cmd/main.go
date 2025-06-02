package main

import (
    "encoding/json"
    "log"
    "net/http"
	    "os"
    "sync"
)


type Transaction struct {
    CustomerName string  `json:"customer_name"`
    Amount       float64 `json:"amount"`
    Location     string  `json:"location"`
    Timestamp    string  `json:"timestamp"`
}



var mu sync.Mutex // to avoid race conditions when writing to file

func ingestHandler(w http.ResponseWriter, r *http.Request) {
    var tx Transaction
    if err := json.NewDecoder(r.Body).Decode(&tx); err != nil {
        http.Error(w, "Invalid input", http.StatusBadRequest)
        return
    }

    mu.Lock()
    defer mu.Unlock()

    file, err := os.OpenFile("transactions.json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        http.Error(w, "Failed to save transaction", http.StatusInternalServerError)
        return
    }
    defer file.Close()

    data, _ := json.Marshal(tx)
    file.Write(append(data, '\n'))

    log.Printf("📥 Received transaction from %s: %.2f SAR in %s", tx.CustomerName, tx.Amount, tx.Location)
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}


func main() {
    http.HandleFunc("/api/ingest", ingestHandler)
    log.Println("🚀 Server started on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
