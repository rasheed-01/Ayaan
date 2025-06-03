package main

import (
    "log"
    "net/http"
    "os"
)

type Transaction struct {
    CustomerName string  `json:"customer_name"`
    Amount       float64 `json:"amount"`
    Location     string  `json:"location"`
    Timestamp    string  `json:"timestamp"`
}

func enableCors(w http.ResponseWriter) {
    w.Header().Set("Access-Control-Allow-Origin", "*")
}

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
    http.HandleFunc("/transactions", func(w http.ResponseWriter, r *http.Request) {
        // Your handler logic
        w.Write([]byte(`{"message":"Hello from Render!"}`))
    })

    log.Printf("Server running on port %s", port)
    log.Fatal(http.ListenAndServe(":" + port, nil))
}
